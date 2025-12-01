"""
基金数据刷新服务 V3
使用动态注册机制，消除代码重复
"""
import logging
from typing import Dict, Any, List, Optional
import asyncio

from app.core.database import get_mongo_db
from app.utils.task_manager import get_task_manager
from app.services.data_sources.base_service import BaseService
from app.services.data_sources.funds.provider_registry import (
    get_provider_class,
    get_collection_definitions,
)
from app.services.data_sources.funds.service_registry import get_service_class
from app.exceptions.funds import (
    FundCollectionNotFound,
    FundDataUpdateError,
)

logger = logging.getLogger(__name__)


class FundRefreshService:
    """基金数据刷新服务 V3 - 使用动态注册"""
    
    def __init__(self, db=None, current_user=None):
        """
        初始化服务
        
        Args:
            db: MongoDB 数据库实例
            current_user: 当前用户信息
        """
        from app.core.database import get_mongo_db
        self.db = db if db is not None else get_mongo_db()
        self.task_manager = get_task_manager()
        self.current_user = current_user
        self._services_cache: Dict[str, BaseService] = {}
    
    def _get_service(self, collection_name: str) -> Optional[BaseService]:
        """
        动态获取服务实例
        
        优先使用已注册的专门服务类（包含批量更新配置等），
        如果没有专门服务类，则动态创建一个基础服务类。
        
        Args:
            collection_name: 集合名称
            
        Returns:
            服务实例，如果不存在则返回 None
        """
        # 使用缓存
        if collection_name in self._services_cache:
            return self._services_cache[collection_name]
        
        # 优先查找已注册的专门服务类
        service_cls = get_service_class(collection_name)
        
        if not service_cls:
            # 没有专门服务类，动态创建
            provider_cls = get_provider_class(collection_name)
            if not provider_cls:
                logger.warning(f"未找到集合 {collection_name} 的 provider")
                return None
            
            # 动态创建服务类
            service_cls = type(
                f"{collection_name.replace('_', ' ').title().replace(' ', '')}Service",
                (BaseService,),
                {
                    "collection_name": collection_name,
                    "provider_class": provider_cls,
                }
            )
        
        try:
            service = service_cls(self.db, self.current_user)
            self._services_cache[collection_name] = service
            return service
        except Exception as e:
            logger.error(f"创建服务实例失败 {collection_name}: {e}", exc_info=True)
            return None
    
    def get_supported_collections(self) -> List[str]:
        """
        获取所有支持的集合名称
        
        Returns:
            集合名称列表
        """
        return [c["name"] for c in get_collection_definitions()]
    
    async def get_collection_overview(self, collection_name: str) -> Dict[str, Any]:
        """
        获取集合概览信息
        
        Args:
            collection_name: 集合名称
            
        Returns:
            概览信息字典
            
        Raises:
            FundCollectionNotFound: 集合不存在
        """
        service = self._get_service(collection_name)
        if not service:
            raise FundCollectionNotFound(collection_name)
        
        try:
            return await service.get_overview()
        except Exception as e:
            logger.error(f"获取集合概览失败 {collection_name}: {e}", exc_info=True)
            raise FundDataUpdateError(f"获取概览失败: {str(e)}", collection_name)
    
    async def refresh_collection(
        self,
        collection_name: str,
        task_id: str,
        params: Dict[str, Any]
    ) -> None:
        """
        刷新集合数据
        
        Args:
            collection_name: 集合名称
            task_id: 任务ID
            params: 更新参数
            
        Raises:
            FundCollectionNotFound: 集合不存在
            FundDataUpdateError: 更新失败
        """
        service = self._get_service(collection_name)
        if not service:
            raise FundCollectionNotFound(collection_name)
        
        try:
            update_type = params.get("update_type", "batch")
            update_mode = params.get("update_mode", "incremental")  # 默认增量更新
            
            if update_type == "single":
                # 单条更新 - 将 params 作为 **kwargs 传递
                # 开始任务
                self.task_manager.start_task(task_id)
                self.task_manager.update_progress(task_id, 0, 100, "开始单条更新...")
                
                try:
                    result = await service.update_single_data(**params)
                    logger.info(f"单条更新完成 {collection_name}: {result}")
                    
                    # 更新任务状态为成功
                    message = result.get("message", "单条更新完成")
                    inserted = result.get("inserted", 0)
                    if inserted > 0:
                        message = f"成功更新 {inserted} 条数据"
                    
                    self.task_manager.complete_task(
                        task_id,
                        result={
                            "saved": inserted,
                            "message": message
                        },
                        message=message
                    )
                except Exception as e:
                    # 更新任务状态为失败
                    error_msg = str(e)
                    logger.error(f"单条更新失败 {collection_name}: {error_msg}", exc_info=True)
                    self.task_manager.fail_task(task_id, error_msg)
                    raise
            else:
                # 批量更新
                # 开始任务
                self.task_manager.start_task(task_id)
                
                # 如果是全量更新，先清除数据
                if update_mode == "full":
                    self.task_manager.update_progress(task_id, 0, 100, "开始全量更新：正在清除现有数据...")
                    try:
                        clear_result = await service.clear_data()
                        if clear_result.get("success"):
                            deleted_count = clear_result.get("deleted_count", 0)
                            logger.info(f"[{collection_name}] 全量更新：已清除 {deleted_count} 条数据")
                            self.task_manager.update_progress(task_id, 5, 100, f"已清除 {deleted_count} 条数据，开始增量更新...")
                        else:
                            logger.warning(f"[{collection_name}] 全量更新：清除数据失败，继续增量更新")
                            self.task_manager.update_progress(task_id, 5, 100, "清除数据失败，继续增量更新...")
                    except Exception as e:
                        logger.error(f"[{collection_name}] 全量更新：清除数据异常: {e}", exc_info=True)
                        self.task_manager.update_progress(task_id, 5, 100, "清除数据异常，继续增量更新...")
                else:
                    self.task_manager.update_progress(task_id, 0, 100, "开始增量更新...")
                
                # 执行批量更新（将 params 作为 **kwargs 传递）
                result = await service.update_batch_data(task_id=task_id, **params)
                logger.info(f"批量更新完成 {collection_name}: {result}")
                
        except FundCollectionNotFound:
            raise
        except Exception as e:
            logger.error(f"刷新集合失败 {collection_name}: {e}", exc_info=True)
            raise FundDataUpdateError(str(e), collection_name)
    
    def clear_cache(self):
        """清空服务缓存"""
        self._services_cache.clear()
        logger.info("已清空服务缓存")
