"""
股票数据刷新服务
动态加载 data_sources/stocks/services 目录中的所有服务
支持 380 个股票数据集合（100% 覆盖率）
"""
import logging
import importlib
import os
from typing import Dict, Any, Type, Optional
import asyncio

from app.core.database import get_mongo_db
from app.utils.task_manager import get_task_manager
from app.config.stock_update_config import get_collection_update_config

logger = logging.getLogger("webapi")


def _snake_to_pascal(name: str) -> str:
    """将下划线命名转换为帕斯卡命名（大驼峰）"""
    return ''.join(word.capitalize() for word in name.split('_'))


def _load_service_classes() -> Dict[str, Type]:
    """
    动态加载所有股票数据服务类
    
    Returns:
        集合名称到服务类的映射
    """
    service_classes = {}
    services_dir = os.path.join(
        os.path.dirname(__file__),
        "data_sources", "stocks", "services"
    )
    
    if not os.path.exists(services_dir):
        logger.warning(f"服务目录不存在: {services_dir}")
        return service_classes
    
    for filename in os.listdir(services_dir):
        if not filename.endswith('_service.py'):
            continue
        if filename.startswith('__') or filename == 'base_service.py':
            continue
        
        # 提取集合名称：stock_zh_a_spot_em_service.py -> stock_zh_a_spot_em
        collection_name = filename[:-11]  # 移除 _service.py
        
        # 构建类名：stock_zh_a_spot_em -> StockZhASpotEmService
        class_name = _snake_to_pascal(collection_name) + 'Service'
        
        # 动态导入模块
        module_name = f"app.services.data_sources.stocks.services.{filename[:-3]}"
        try:
            module = importlib.import_module(module_name)
            service_class = getattr(module, class_name, None)
            if service_class:
                service_classes[collection_name] = service_class
        except Exception as e:
            logger.debug(f"加载服务 {collection_name} 失败: {e}")
    
    logger.info(f"已加载 {len(service_classes)} 个股票数据服务")
    return service_classes


# 在模块加载时预加载所有服务类
_SERVICE_CLASSES: Dict[str, Type] = {}


def _ensure_service_classes():
    """确保服务类已加载"""
    global _SERVICE_CLASSES
    if not _SERVICE_CLASSES:
        _SERVICE_CLASSES = _load_service_classes()


class StockRefreshService:
    """股票数据刷新服务 - 动态加载所有股票数据集合的服务"""
    
    # 前端特有的参数，不应传递给 akshare 函数
    FRONTEND_ONLY_PARAMS = {
        'batch', 'batch_update', 'batch_size', 'concurrency', 'delay', 'update_type',
        'page', 'limit', 'skip', 'filters', 'sort', 'order',
        'task_id', 'callback', 'async', 'timeout', '_t', '_timestamp',
        'force', 'clear_first', 'overwrite', 'mode'
    }
    
    def __init__(self, db=None):
        self.db = db if db is not None else get_mongo_db()
        self.task_manager = get_task_manager()
        
        # 确保服务类已加载
        _ensure_service_classes()
        
        # 初始化服务实例（懒加载）
        self._services: Dict[str, Any] = {}
    
    def _get_service(self, collection_name: str):
        """获取或创建服务实例"""
        if collection_name not in self._services:
            service_class = _SERVICE_CLASSES.get(collection_name)
            if service_class:
                self._services[collection_name] = service_class(self.db)
            else:
                return None
        return self._services[collection_name]
    
    async def refresh_collection(
        self,
        collection_name: str,
        task_id: str,
        params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        刷新指定的股票数据集合
        
        Args:
            collection_name: 集合名称
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.start_task(task_id)
            self.task_manager.update_progress(task_id, 0, 100, f"开始刷新 {collection_name}...")
            
            # 获取服务
            service = self._get_service(collection_name)
            if service is None:
                raise ValueError(f"未找到集合 {collection_name} 的服务")
            
            # 更新进度
            self.task_manager.update_progress(task_id, 10, 100, f"正在获取 {collection_name} 数据...")
            
            # 判断是批量更新还是单条更新
            is_batch = (
                params.get("batch") or 
                params.get("batch_update") or 
                params.get("update_type") == "batch"
            ) if params else False
            
            # 过滤掉前端特有的参数
            api_params = {}
            if params:
                api_params = {
                    k: v for k, v in params.items() 
                    if k not in self.FRONTEND_ONLY_PARAMS
                }
                if is_batch and "concurrency" in params:
                    api_params["concurrency"] = params["concurrency"]
                logger.info(f"[参数过滤] 原始参数: {params}, 过滤后: {api_params}")
            
            # 调用服务刷新数据
            # 现有服务使用 refresh_data 方法
            if hasattr(service, "refresh_data"):
                result = await service.refresh_data(**api_params)
            elif is_batch and hasattr(service, "update_batch_data"):
                result = await service.update_batch_data(task_id=task_id, **api_params)
            elif hasattr(service, "update_single_data"):
                result = await service.update_single_data(**api_params)
            else:
                raise ValueError(f"服务 {collection_name} 没有可用的刷新方法")
            
            # 更新任务状态
            if result.get("success", True):
                self.task_manager.update_progress(
                    task_id, 100, 100, 
                    f"成功刷新 {collection_name}，处理 {result.get('inserted', 0)} 条数据"
                )
                self.task_manager.complete_task(task_id, result=result)
            else:
                self.task_manager.fail_task(task_id, result.get("message", "刷新失败"))
            
            return result
            
        except Exception as e:
            logger.error(f"刷新 {collection_name} 失败: {e}", exc_info=True)
            self.task_manager.fail_task(task_id, str(e))
            return {"success": False, "message": str(e)}
    
    async def get_collection_overview(self, collection_name: str) -> Dict[str, Any]:
        """获取集合数据概览"""
        service = self._get_service(collection_name)
        if service is None:
            raise ValueError(f"未找到集合 {collection_name} 的服务")
        
        if hasattr(service, "get_overview"):
            return await service.get_overview()
        return {"total_count": 0, "message": "不支持概览"}
    
    async def get_collection_data(
        self,
        collection_name: str,
        skip: int = 0,
        limit: int = 100,
        filters: Dict = None
    ) -> Dict[str, Any]:
        """获取集合数据"""
        service = self._get_service(collection_name)
        if service is None:
            raise ValueError(f"未找到集合 {collection_name} 的服务")
        
        if hasattr(service, "get_data"):
            return await service.get_data(skip=skip, limit=limit, filters=filters)
        return {"items": [], "total": 0}
    
    async def clear_collection(self, collection_name: str) -> Dict[str, Any]:
        """清空集合数据"""
        service = self._get_service(collection_name)
        if service is None:
            raise ValueError(f"未找到集合 {collection_name} 的服务")
        
        if hasattr(service, "clear_data"):
            return await service.clear_data()
        return {"success": False, "message": "不支持清空"}
    
    def get_supported_collections(self) -> list:
        """获取支持的所有数据集合列表"""
        return list(_SERVICE_CLASSES.keys())
    
    def get_collection_count(self) -> int:
        """获取支持的数据集合数量"""
        return len(_SERVICE_CLASSES)
    
    @classmethod
    def get_update_config(cls, collection_name: str) -> Dict[str, Any]:
        """获取集合的更新配置"""
        return get_collection_update_config(collection_name)
