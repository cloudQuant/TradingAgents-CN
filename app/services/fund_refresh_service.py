"""
基金数据刷新服务
负责调用akshare获取基金数据并保存到数据库
"""
import logging
from typing import Dict, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor

from app.core.database import get_mongo_db
from app.services.fund_data_service import FundDataService
from app.utils.task_manager import get_task_manager

logger = logging.getLogger("webapi")

# 线程池，用于执行同步的akshare调用
_executor = ThreadPoolExecutor(max_workers=5)


class FundRefreshService:
    """基金数据刷新服务"""
    
    def __init__(self, db=None):
        self.db = db or get_mongo_db()
        self.data_service = FundDataService(self.db)
        self.task_manager = get_task_manager()
    
    async def refresh_collection(
        self,
        collection_name: str,
        task_id: str,
        params: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        刷新指定的基金数据集合
        
        Args:
            collection_name: 集合名称
            task_id: 任务ID
            params: 参数
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(task_id, 0, 100, f"开始刷新 {collection_name}...")
            
            # 根据collection_name调用不同的刷新方法
            handlers = {
                "fund_name_em": self._refresh_fund_name_em,
                "fund_basic_info": self._refresh_fund_basic_info,
            }
            
            handler = handlers.get(collection_name)
            if not handler:
                raise ValueError(f"不支持的集合类型: {collection_name}")
            
            result = await handler(task_id, params or {})
            
            self.task_manager.complete_task(task_id, result)
            return result
            
        except Exception as e:
            logger.error(f"刷新集合 {collection_name} 失败: {e}", exc_info=True)
            self.task_manager.fail_task(task_id, str(e))
            raise
    
    async def _refresh_fund_name_em(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新基金基本信息数据
        使用akshare的fund_name_em接口
        
        Args:
            task_id: 任务ID
            params: 参数（该接口无需参数）
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(task_id, 10, 100, "正在从东方财富网获取基金基本信息...")
            
            # 在线程池中调用akshare（因为akshare是同步的）
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_name_em)
            
            if df is None or df.empty:
                raise ValueError("未获取到基金基本信息数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条基金数据，正在保存...")
            
            # 保存数据
            saved_count = await self.data_service.save_fund_name_em_data(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条基金基本信息"
            }
            
        except Exception as e:
            logger.error(f"刷新基金基本信息失败: {e}", exc_info=True)
            raise
    
    def _fetch_fund_name_em(self):
        """
        调用akshare获取基金基本信息（同步方法，在线程池中执行）
        
        Returns:
            DataFrame: 基金基本信息数据
        """
        try:
            import akshare as ak
            logger.info("开始调用akshare获取基金基本信息...")
            df = ak.fund_name_em()
            logger.info(f"成功获取 {len(df)} 条基金基本信息")
            return df
        except Exception as e:
            logger.error(f"调用akshare获取基金基本信息失败: {e}", exc_info=True)
            raise
    
    async def _refresh_fund_basic_info(self, task_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        刷新fund_basic_info基金基本信息数据
        使用akshare的fund_name_em接口（与fund_name_em相同的数据源）
        
        Args:
            task_id: 任务ID
            params: 参数（该接口无需参数）
            
        Returns:
            刷新结果
        """
        try:
            self.task_manager.update_progress(task_id, 10, 100, "正在从东方财富网获取基金基本信息...")
            
            # 在线程池中调用akshare（因为akshare是同步的）
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(_executor, self._fetch_fund_name_em)
            
            if df is None or df.empty:
                raise ValueError("未获取到基金基本信息数据")
            
            self.task_manager.update_progress(task_id, 50, 100, f"获取到 {len(df)} 条基金数据，正在保存到fund_basic_info集合...")
            
            # 保存数据到fund_basic_info集合
            saved_count = await self.data_service.save_fund_basic_info_data(df)
            
            self.task_manager.update_progress(task_id, 100, 100, f"成功保存 {saved_count} 条数据")
            
            return {
                'success': True,
                'saved': saved_count,
                'message': f"成功更新 {saved_count} 条基金基本信息到fund_basic_info集合"
            }
            
        except Exception as e:
            logger.error(f"刷新fund_basic_info基金基本信息失败: {e}", exc_info=True)
            raise
