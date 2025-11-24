"""
基金公告人事调整批量更新服务
支持单个更新和批量更新
"""

import logging
import asyncio
from typing import Dict, Any, List
import akshare as ak
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

from app.services.fund_data_service import FundDataService
from app.utils.task_manager import TaskManager

logger = logging.getLogger("webapi")

# 线程池
_executor = ThreadPoolExecutor(max_workers=3)


class FundAnnouncementPersonnelBatchService:
    """基金公告人事调整批量更新服务"""
    
    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager
        self.data_service = FundDataService()
    
    def _fetch_single_fund_announcement(self, fund_code: str) -> pd.DataFrame:
        """
        获取单个基金的公告人事调整数据
        
        注意：akshare 的 fund_announcement_personnel_em 接口不支持单个基金查询
        需要获取全量数据后筛选
        """
        try:
            logger.info(f"获取基金 {fund_code} 的公告人事调整数据...")
            df = ak.fund_announcement_personnel_em()
            
            if df is None or df.empty:
                logger.warning(f"未获取到任何公告数据")
                return pd.DataFrame()
            
            # 筛选指定基金
            df_filtered = df[df['基金代码'] == fund_code].copy()
            logger.info(f"基金 {fund_code} 有 {len(df_filtered)} 条公告人事调整记录")
            
            return df_filtered
            
        except Exception as e:
            logger.error(f"获取基金 {fund_code} 公告数据失败: {e}", exc_info=True)
            return pd.DataFrame()
    
    def _fetch_batch_fund_announcement(self, fund_codes: List[str]) -> pd.DataFrame:
        """
        批量获取多个基金的公告人事调整数据
        """
        try:
            logger.info(f"批量获取 {len(fund_codes)} 个基金的公告人事调整数据...")
            df = ak.fund_announcement_personnel_em()
            
            if df is None or df.empty:
                logger.warning(f"未获取到任何公告数据")
                return pd.DataFrame()
            
            # 筛选指定基金列表
            df_filtered = df[df['基金代码'].isin(fund_codes)].copy()
            logger.info(f"筛选出 {len(df_filtered)} 条公告人事调整记录")
            
            return df_filtered
            
        except Exception as e:
            logger.error(f"批量获取基金公告数据失败: {e}", exc_info=True)
            return pd.DataFrame()
    
    async def update_single_fund(self, task_id: str, fund_code: str) -> Dict[str, Any]:
        """
        更新单个基金的公告人事调整数据
        
        Args:
            task_id: 任务ID
            fund_code: 基金代码
            
        Returns:
            更新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 10, 100, 
                f"开始获取基金 {fund_code} 的公告人事调整数据..."
            )
            
            # 在线程池中执行同步IO操作
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(
                _executor, 
                self._fetch_single_fund_announcement, 
                fund_code
            )
            
            if df.empty:
                self.task_manager.update_progress(
                    task_id, 100, 100, 
                    f"基金 {fund_code} 没有公告人事调整数据"
                )
                return {
                    'success': True,
                    'fund_code': fund_code,
                    'saved': 0,
                    'message': f"基金 {fund_code} 没有公告人事调整数据"
                }
            
            self.task_manager.update_progress(
                task_id, 50, 100, 
                f"获取到 {len(df)} 条数据，正在保存..."
            )
            
            # 保存数据
            def on_save_progress(current, total, percentage, message):
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_fund_announcement_personnel_em_data(
                df, progress_callback=on_save_progress
            )
            
            self.task_manager.update_progress(
                task_id, 100, 100, 
                f"成功保存 {saved_count} 条数据"
            )
            
            return {
                'success': True,
                'fund_code': fund_code,
                'saved': saved_count,
                'message': f"成功更新基金 {fund_code} 的 {saved_count} 条公告人事调整数据"
            }
            
        except Exception as e:
            error_msg = f"更新基金 {fund_code} 公告数据失败: {str(e)}"
            logger.error(error_msg, exc_info=True)
            self.task_manager.update_progress(task_id, 0, 100, error_msg)
            raise
    
    async def update_batch_funds(
        self, 
        task_id: str, 
        fund_codes: List[str],
        batch_size: int = 100
    ) -> Dict[str, Any]:
        """
        批量更新多个基金的公告人事调整数据
        
        Args:
            task_id: 任务ID
            fund_codes: 基金代码列表
            batch_size: 每批处理的数量
            
        Returns:
            更新结果
        """
        try:
            total_funds = len(fund_codes)
            self.task_manager.update_progress(
                task_id, 5, 100, 
                f"准备批量更新 {total_funds} 个基金的公告人事调整数据..."
            )
            
            # 获取全量数据并筛选
            loop = asyncio.get_event_loop()
            df = await loop.run_in_executor(
                _executor, 
                self._fetch_batch_fund_announcement, 
                fund_codes
            )
            
            if df.empty:
                self.task_manager.update_progress(
                    task_id, 100, 100, 
                    f"这 {total_funds} 个基金没有公告人事调整数据"
                )
                return {
                    'success': True,
                    'total_funds': total_funds,
                    'saved': 0,
                    'message': f"这 {total_funds} 个基金没有公告人事调整数据"
                }
            
            self.task_manager.update_progress(
                task_id, 50, 100, 
                f"获取到 {len(df)} 条数据，正在保存..."
            )
            
            # 保存数据
            def on_save_progress(current, total, percentage, message):
                overall_progress = 50 + int(percentage * 0.5)
                self.task_manager.update_progress(task_id, overall_progress, 100, message)
            
            saved_count = await self.data_service.save_fund_announcement_personnel_em_data(
                df, progress_callback=on_save_progress
            )
            
            # 统计每个基金的数据
            fund_counts = df['基金代码'].value_counts().to_dict()
            
            self.task_manager.update_progress(
                task_id, 100, 100, 
                f"成功保存 {saved_count} 条数据"
            )
            
            return {
                'success': True,
                'total_funds': total_funds,
                'saved': saved_count,
                'fund_counts': fund_counts,
                'message': f"成功更新 {total_funds} 个基金的 {saved_count} 条公告人事调整数据"
            }
            
        except Exception as e:
            error_msg = f"批量更新基金公告数据失败: {str(e)}"
            logger.error(error_msg, exc_info=True)
            self.task_manager.update_progress(task_id, 0, 100, error_msg)
            raise
    
    async def update_incremental(
        self, 
        task_id: str, 
        limit: int = None
    ) -> Dict[str, Any]:
        """
        增量更新：获取 fund_name_em 中的所有基金代码，批量更新公告数据
        
        Args:
            task_id: 任务ID
            limit: 限制更新的基金数量（测试用）
            
        Returns:
            更新结果
        """
        try:
            self.task_manager.update_progress(
                task_id, 5, 100, 
                "正在从 fund_name_em 获取基金代码列表..."
            )
            
            # 获取所有基金代码
            from app.core.database import get_mongo_db
            db = get_mongo_db()
            col_fund_name = db.get_collection("fund_name_em")
            
            fund_codes = []
            async for doc in col_fund_name.find({}, {'基金代码': 1}):
                code = doc.get('基金代码', '') or doc.get('code', '')
                if code:
                    fund_codes.append(str(code))
            
            if limit:
                fund_codes = fund_codes[:limit]
            
            total_funds = len(fund_codes)
            
            if total_funds == 0:
                self.task_manager.update_progress(
                    task_id, 100, 100, 
                    "fund_name_em 中没有基金代码"
                )
                return {
                    'success': True,
                    'total_funds': 0,
                    'saved': 0,
                    'message': "fund_name_em 中没有基金代码"
                }
            
            logger.info(f"从 fund_name_em 获取到 {total_funds} 个基金代码")
            
            # 批量更新
            return await self.update_batch_funds(task_id, fund_codes)
            
        except Exception as e:
            error_msg = f"增量更新失败: {str(e)}"
            logger.error(error_msg, exc_info=True)
            self.task_manager.update_progress(task_id, 0, 100, error_msg)
            raise
