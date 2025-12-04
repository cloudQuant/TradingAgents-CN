"""
债券数据刷新服务
重构版：使用动态注册机制，自动发现和加载Service类
包含全部34个债券数据集合
"""
import logging
from typing import Dict, Any, Optional, Type
import asyncio

from app.core.database import get_mongo_db
from app.utils.task_manager import get_task_manager
from app.services.data_sources.base_service import BaseService

logger = logging.getLogger("webapi")


class BondRefreshService:
    """债券数据刷新服务（使用动态注册机制）"""
    
    def __init__(self, db=None, current_user=None):
        self.db = db if db is not None else get_mongo_db()
        self.current_user = current_user
        self.task_manager = get_task_manager()
        self._services: Dict[str, BaseService] = {}  # 服务实例缓存
        self._service_classes: Dict[str, Type[BaseService]] = None  # Service类注册表
    
    def _get_service_classes(self) -> Dict[str, Type[BaseService]]:
        """获取所有已注册的Service类（使用动态发现）"""
        if self._service_classes is not None:
            return self._service_classes
        
        from app.services.data_sources.bonds.service_registry import get_all_service_classes
        self._service_classes = get_all_service_classes()
        logger.info(f"[BondRefreshService] 动态发现 {len(self._service_classes)} 个 Service 类")
        
        return self._service_classes
    
    def _get_service(self, collection_name: str) -> Optional[BaseService]:
        """获取或创建Service实例"""
        if collection_name in self._services:
            return self._services[collection_name]
        
        service_classes = self._get_service_classes()
        service_cls = service_classes.get(collection_name)
        
        if service_cls is None:
            logger.warning(f"[BondRefreshService] 未找到 {collection_name} 的 Service 类")
            return None
        
        try:
            # 创建Service实例
            service = service_cls(self.db, self.current_user)
            self._services[collection_name] = service
            return service
        except Exception as e:
            logger.error(f"[BondRefreshService] 创建 {collection_name} Service 实例失败: {e}")
            return None
    
    def get_supported_collections(self) -> list:
        """获取支持的所有数据集合列表"""
        return list(self._get_service_classes().keys())
    
    # 前端特有的参数，不应传递给 akshare 函数
    FRONTEND_ONLY_PARAMS = {
        # 批量更新控制参数
        'batch', 'batch_update', 'batch_size', 'delay', 'update_type', 'update_mode',
        # 分页和过滤参数
        'page', 'limit', 'skip', 'filters', 'sort', 'order',
        # 任务和回调参数
        'task_id', 'callback', 'async', 'timeout', '_t', '_timestamp',
        # 更新控制参数
        'force', 'clear_first', 'overwrite', 'mode'
    }
    
    async def refresh_collection(
        self,
        collection_name: str,
        task_id: str,
        params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        刷新指定的债券数据集合
        
        Args:
            collection_name: 集合名称
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            service = self._get_service(collection_name)
            if not service:
                raise ValueError(f"未找到集合 {collection_name} 的服务")
            
            params = params or {}
            update_type = params.get("update_type", "batch")
            update_mode = params.get("update_mode", "incremental")
            
            if update_type == "single":
                # 单条更新
                self.task_manager.start_task(task_id)
                self.task_manager.update_progress(task_id, 0, 100, "开始单条更新...")
                
                try:
                    result = await service.update_single_data(**params)
                    logger.info(f"单条更新完成 {collection_name}: {result}")
                    
                    message = result.get("message", "单条更新完成")
                    inserted = result.get("inserted", 0)
                    if inserted > 0:
                        message = f"成功更新 {inserted} 条数据"
                    
                    self.task_manager.complete_task(
                        task_id,
                        result={"saved": inserted, "message": message},
                        message=message
                    )
                except Exception as e:
                    error_msg = str(e)
                    logger.error(f"单条更新失败 {collection_name}: {error_msg}", exc_info=True)
                    self.task_manager.fail_task(task_id, error_msg)
                    raise
            else:
                # 批量更新
                self.task_manager.start_task(task_id)
                
                # 如果是全量更新，先清除数据
                if update_mode == "full":
                    self.task_manager.update_progress(task_id, 0, 100, "开始全量更新：正在清除现有数据...")
                    try:
                        clear_result = await service.clear_data()
                        if clear_result.get("success"):
                            deleted_count = clear_result.get("deleted_count", 0)
                            logger.info(f"[{collection_name}] 全量更新：已清除 {deleted_count} 条数据")
                            self.task_manager.update_progress(task_id, 5, 100, f"已清除 {deleted_count} 条数据，开始获取新数据...")
                    except Exception as e:
                        logger.error(f"[{collection_name}] 全量更新：清除数据异常: {e}", exc_info=True)
                        self.task_manager.update_progress(task_id, 5, 100, "清除数据异常，继续增量更新...")
                else:
                    self.task_manager.update_progress(task_id, 0, 100, "开始增量更新...")
                
                # 执行批量更新
                result = await service.update_batch_data(task_id=task_id, **params)
                logger.info(f"批量更新完成 {collection_name}: {result}")
            
            return result
            
        except Exception as e:
            logger.error(f"刷新集合失败 {collection_name}: {e}", exc_info=True)
            raise
    
    async def get_collection_overview(self, collection_name: str) -> Dict[str, Any]:
        """获取集合数据概览"""
        service = self._get_service(collection_name)
        if not service:
            raise ValueError(f"未找到集合 {collection_name} 的服务")
        return await service.get_overview()
    
    async def get_collection_data(
        self,
        collection_name: str,
        skip: int = 0,
        limit: int = 100,
        filters: Dict = None
    ) -> Dict[str, Any]:
        """获取集合数据"""
        service = self._get_service(collection_name)
        if not service:
            raise ValueError(f"未找到集合 {collection_name} 的服务")
        return await service.get_data(skip=skip, limit=limit, filters=filters)
    
    async def clear_collection(self, collection_name: str) -> Dict[str, Any]:
        """清空集合数据"""
        service = self._get_service(collection_name)
        if not service:
            raise ValueError(f"未找到集合 {collection_name} 的服务")
        return await service.clear_data()
    
    def get_collection_count(self) -> int:
        """获取支持的数据集合数量"""
        return len(self._get_service_classes())
