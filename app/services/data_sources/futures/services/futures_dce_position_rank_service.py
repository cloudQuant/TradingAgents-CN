"""
大连商品交易所持仓排名服务
"""
import asyncio
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_dce_position_rank_provider import FuturesDcePositionRankProvider
from app.utils.task_manager import get_task_manager

logger = logging.getLogger(__name__)


class FuturesDcePositionRankService(BaseFuturesService):
    """大连商品交易所持仓排名服务"""
    
    def __init__(self, db: AsyncIOMotorClient):
        provider = FuturesDcePositionRankProvider()
        super().__init__(db, "futures_dce_position_rank", provider)
    
    def _get_trading_days(self, start_date: str, end_date: str) -> List[str]:
        """
        获取日期范围内的交易日（简单实现，排除周末）
        
        Args:
            start_date: 开始日期，格式YYYYMMDD
            end_date: 结束日期，格式YYYYMMDD
        """
        start = datetime.strptime(start_date, "%Y%m%d")
        end = datetime.strptime(end_date, "%Y%m%d")
        
        trading_days = []
        current = start
        while current <= end:
            # 排除周末
            if current.weekday() < 5:  # 0-4 为周一到周五
                trading_days.append(current.strftime("%Y%m%d"))
            current += timedelta(days=1)
        
        return trading_days
    
    async def update_batch_data(
        self, 
        task_id: str = None,
        start_date: str = None,
        end_date: str = None,
        days: int = 5,
        concurrency: int = 2,
        **kwargs
    ) -> Dict[str, Any]:
        """
        批量更新多个日期的持仓排名数据
        
        Args:
            task_id: 任务ID
            start_date: 开始日期，格式YYYYMMDD
            end_date: 结束日期，格式YYYYMMDD
            days: 如果不指定日期范围，默认更新最近N天
            concurrency: 并发数，默认2（避免频繁请求）
        """
        try:
            task_manager = get_task_manager() if task_id else None
            
            # 确定日期范围
            if not end_date:
                end_date = datetime.now().strftime("%Y%m%d")
            if not start_date:
                start = datetime.strptime(end_date, "%Y%m%d") - timedelta(days=days)
                start_date = start.strftime("%Y%m%d")
            
            # 获取交易日列表
            date_list = self._get_trading_days(start_date, end_date)
            total = len(date_list)
            
            if task_manager and task_id:
                task_manager.update_progress(task_id, 0, total, f"准备更新 {total} 个交易日的持仓排名...")
            
            logger.info(f"[{self.collection_name}] 开始批量更新 {total} 个交易日: {start_date} - {end_date}")
            
            results = {
                "success": True,
                "total": total,
                "succeeded": 0,
                "failed": 0,
                "inserted": 0,
                "errors": []
            }
            
            semaphore = asyncio.Semaphore(concurrency)
            
            async def fetch_date(date: str, index: int):
                async with semaphore:
                    try:
                        result = await self.update_single_data(date=date)
                        if result.get("success"):
                            results["succeeded"] += 1
                            results["inserted"] += result.get("inserted", 0)
                        else:
                            results["failed"] += 1
                            results["errors"].append({"date": date, "error": result.get("message")})
                        
                        if task_manager and task_id:
                            task_manager.update_progress(
                                task_id, index + 1, total,
                                f"已完成 {date}，进度 {index + 1}/{total}"
                            )
                        
                        # 添加延迟避免API限流
                        await asyncio.sleep(0.5)
                        
                    except Exception as e:
                        results["failed"] += 1
                        results["errors"].append({"date": date, "error": str(e)})
                        logger.error(f"更新日期 {date} 失败: {e}")
            
            # 顺序执行（避免并发过多）
            for i, date in enumerate(date_list):
                await fetch_date(date, i)
            
            if task_manager and task_id:
                task_manager.update_progress(
                    task_id, total, total,
                    f"批量更新完成: 成功 {results['succeeded']} 天，插入 {results['inserted']} 条"
                )
                task_manager.complete_task(task_id, result=results)
            
            logger.info(f"[{self.collection_name}] 批量更新完成: {results}")
            return results
            
        except Exception as e:
            logger.error(f"[{self.collection_name}] 批量更新失败: {e}", exc_info=True)
            if task_manager and task_id:
                task_manager.fail_task(task_id, str(e))
            return {"success": False, "message": str(e), "inserted": 0}
