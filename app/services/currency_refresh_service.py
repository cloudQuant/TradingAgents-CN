"""
外汇数据刷新服务
参考基金刷新服务实现，统一管理外汇数据集合的刷新
"""
import logging
from typing import Dict, Any

from app.core.database import get_mongo_db
from app.utils.task_manager import get_task_manager

# 导入所有外汇服务
from app.services.data_sources.currencies.services.currency_latest_service import CurrencyLatestService
from app.services.data_sources.currencies.services.currency_history_service import CurrencyHistoryService
from app.services.data_sources.currencies.services.currency_time_series_service import CurrencyTimeSeriesService
from app.services.data_sources.currencies.services.currency_currencies_service import CurrencyCurrenciesService
from app.services.data_sources.currencies.services.currency_convert_service import CurrencyConvertService

logger = logging.getLogger("webapi")


class CurrencyRefreshService:
    """外汇数据刷新服务"""
    
    def __init__(self, db=None):
        self.db = db if db is not None else get_mongo_db()
        self.task_manager = get_task_manager()
        
        # 初始化所有5个服务
        self.services = {
            "currency_latest": CurrencyLatestService(self.db),
            "currency_history": CurrencyHistoryService(self.db),
            "currency_time_series": CurrencyTimeSeriesService(self.db),
            "currency_currencies": CurrencyCurrenciesService(self.db),
            "currency_convert": CurrencyConvertService(self.db),
        }
    
    # 前端特有的参数，不应传递给 akshare 函数
    FRONTEND_ONLY_PARAMS = {
        'batch', 'batch_update', 'update_type', 'concurrency',
        'page', 'limit', 'skip', 'filters', 'sort', 'order',
        'task_id', 'callback', 'async', 'timeout', '_t', '_timestamp',
        'force', 'clear_first', 'overwrite', 'mode'
    }
    
    async def refresh_collection(
        self,
        collection_name: str,
        task_id: str,
        params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        刷新指定的外汇数据集合
        
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
            
            # 检查服务是否存在
            if collection_name not in self.services:
                raise ValueError(f"未找到集合 {collection_name} 的服务")
            
            service = self.services[collection_name]
            
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
                # 对于批量更新，保留 concurrency 参数
                if is_batch and "concurrency" in params:
                    api_params["concurrency"] = params["concurrency"]
                logger.info(f"[参数过滤] 原始参数: {params}, 过滤后: {api_params}, 批量更新: {is_batch}")
            
            # 调用服务刷新数据
            if is_batch and hasattr(service, "update_batch_data"):
                logger.info(f"[{collection_name}] 调用批量更新方法 update_batch_data")
                result = await service.update_batch_data(task_id=task_id, **api_params)
            else:
                logger.info(f"[{collection_name}] 调用单条更新方法 update_single_data")
                result = await service.update_single_data(**api_params)
                
                # 单条更新需要在这里处理任务状态
                if result.get("success"):
                    self.task_manager.update_progress(
                        task_id, 100, 100, 
                        f"成功刷新 {collection_name}，插入 {result.get('inserted', 0)} 条数据"
                    )
                    self.task_manager.complete_task(task_id)
                else:
                    self.task_manager.fail_task(task_id, result.get("message", "刷新失败"))
            
            return result
            
        except Exception as e:
            logger.error(f"刷新 {collection_name} 失败: {e}", exc_info=True)
            self.task_manager.fail_task(task_id, str(e))
            raise
    
    async def get_collection_overview(self, collection_name: str) -> Dict[str, Any]:
        """获取集合数据概览"""
        if collection_name not in self.services:
            raise ValueError(f"未找到集合 {collection_name} 的服务")
        
        service = self.services[collection_name]
        return await service.get_overview()
    
    async def get_collection_data(
        self,
        collection_name: str,
        skip: int = 0,
        limit: int = 100,
        filters: Dict = None
    ) -> Dict[str, Any]:
        """获取集合数据"""
        if collection_name not in self.services:
            raise ValueError(f"未找到集合 {collection_name} 的服务")
        
        service = self.services[collection_name]
        return await service.get_data(skip=skip, limit=limit, filters=filters)
    
    async def clear_collection(self, collection_name: str) -> Dict[str, Any]:
        """清空集合数据"""
        if collection_name not in self.services:
            raise ValueError(f"未找到集合 {collection_name} 的服务")
        
        service = self.services[collection_name]
        return await service.clear_data()
    
    def get_supported_collections(self) -> list:
        """获取支持的所有数据集合列表"""
        return list(self.services.keys())
    
    def get_collection_count(self) -> int:
        """获取支持的数据集合数量"""
        return len(self.services)
