"""期货规则-交易日历表数据服务

支持批量更新：
- 从数据集合中获取最新日期作为开始日期
- 如果没有数据，从 2010-01-01 开始
- 遍历到今天的所有工作日（周一至周五）
- 并发调用 akshare 的 futures_rule(date=xxx) 接口
- 默认并发数 3
"""
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple
import asyncio
import logging

from app.services.data_sources.base_service import BaseService
from app.services.data_sources.futures.providers.futures_rule_provider import FuturesRuleProvider
from app.services.database.control_mongodb import ControlMongodb
from app.utils.task_manager import get_task_manager

logger = logging.getLogger(__name__)


class FuturesRuleService(BaseService):
    """期货规则-交易日历表数据服务
    
    支持两种更新模式：
    - 单条更新 (update_type=single): 获取最新数据
    - 批量更新 (update_type=batch): 按日期范围批量获取历史数据
    """
    collection_name = "futures_rule"
    provider_class = FuturesRuleProvider
    
    # 批量更新配置
    batch_concurrency = 3  # 默认并发数
    batch_task_timeout = 60  # 单个任务超时时间（秒）
    batch_start_date = "2010-01-01"  # 默认起始日期
    
    async def get_latest_date_in_collection(self) -> str:
        """获取集合中最新的日期
        
        Returns:
            最新日期字符串 (YYYY-MM-DD 格式)，如果没有数据返回 None
        """
        try:
            # 查找日期字段最大值
            pipeline = [
                {"$match": {"日期": {"$exists": True, "$ne": None}}},
                {"$group": {"_id": None, "max_date": {"$max": "$日期"}}},
            ]
            async for doc in self.collection.aggregate(pipeline):
                max_date = doc.get("max_date")
                if max_date:
                    # 确保返回 YYYY-MM-DD 格式
                    if isinstance(max_date, datetime):
                        return max_date.strftime("%Y-%m-%d")
                    return str(max_date)[:10]
            return None
        except Exception as e:
            logger.error(f"获取最新日期失败: {e}", exc_info=True)
            return None
    
    def generate_weekday_dates(self, start_date: str, end_date: str) -> List[str]:
        """生成日期范围内的所有工作日（周一至周五）
        
        Args:
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            
        Returns:
            工作日日期列表
        """
        dates = []
        current = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        while current <= end:
            # weekday(): 0=周一, 1=周二, ..., 4=周五, 5=周六, 6=周日
            if current.weekday() < 5:  # 周一到周五
                dates.append(current.strftime("%Y-%m-%d"))
            current += timedelta(days=1)
        
        return dates
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """批量更新数据
        
        从集合中获取最新日期，遍历到今天的所有工作日，并发获取数据
        
        Args:
            task_id: 任务ID
            **kwargs: 其他参数，支持:
                - concurrency: 并发数 (默认3)
                - start_date: 自定义开始日期
                - end_date: 自定义结束日期
        """
        task_manager = get_task_manager() if task_id else None
        concurrency = kwargs.get("concurrency", self.batch_concurrency)
        
        try:
            # 1. 确定日期范围
            if task_manager and task_id:
                task_manager.update_progress(task_id, 0, 100, "正在获取日期范围...")
            
            # 获取结束日期（默认今天）
            end_date = kwargs.get("end_date") or datetime.now().strftime("%Y-%m-%d")
            
            # 获取开始日期
            start_date = kwargs.get("start_date")
            if not start_date:
                # 从集合中获取最新日期
                latest_date = await self.get_latest_date_in_collection()
                if latest_date:
                    # 从最新日期的下一天开始
                    latest = datetime.strptime(latest_date, "%Y-%m-%d")
                    start_date = (latest + timedelta(days=1)).strftime("%Y-%m-%d")
                    logger.info(f"[{self.collection_name}] 集合中最新日期: {latest_date}, 从 {start_date} 开始更新")
                else:
                    # 没有数据，从默认起始日期开始
                    start_date = self.batch_start_date
                    logger.info(f"[{self.collection_name}] 集合为空，从 {start_date} 开始更新")
            
            # 检查日期范围是否有效
            if start_date > end_date:
                message = f"数据已是最新，无需更新（最新日期: {kwargs.get('start_date') or start_date}）"
                logger.info(f"[{self.collection_name}] {message}")
                if task_manager and task_id:
                    task_manager.update_progress(task_id, 100, 100, message)
                    task_manager.complete_task(task_id, result={"inserted": 0}, message=message)
                return {"success": True, "message": message, "inserted": 0}
            
            # 2. 生成工作日日期列表
            dates = self.generate_weekday_dates(start_date, end_date)
            
            if not dates:
                message = "没有需要更新的工作日"
                if task_manager and task_id:
                    task_manager.update_progress(task_id, 100, 100, message)
                    task_manager.complete_task(task_id, result={"inserted": 0}, message=message)
                return {"success": True, "message": message, "inserted": 0}
            
            total_dates = len(dates)
            logger.info(f"[{self.collection_name}] 需要更新 {total_dates} 个工作日的数据 ({start_date} ~ {end_date})")
            
            if task_manager and task_id:
                task_manager.update_progress(
                    task_id, 5, 100, 
                    f"需要更新 {total_dates} 个工作日的数据 ({start_date} ~ {end_date})"
                )
            
            # 3. 并发执行
            return await self._execute_date_batch_tasks(
                dates, task_id, task_manager, concurrency
            )
            
        except Exception as e:
            logger.error(f"[{self.collection_name}] 批量更新失败: {e}", exc_info=True)
            if task_manager and task_id:
                task_manager.fail_task(task_id, str(e))
            raise
    
    async def _execute_date_batch_tasks(
        self,
        dates: List[str],
        task_id: str,
        task_manager,
        concurrency: int
    ) -> Dict[str, Any]:
        """并发执行日期批量任务
        
        Args:
            dates: 日期列表
            task_id: 任务ID
            task_manager: 任务管理器
            concurrency: 并发数
        """
        semaphore = asyncio.Semaphore(concurrency)
        total_inserted = 0
        processed = 0
        success_count = 0
        failed = 0
        empty_count = 0  # 空数据的日期数
        lock = asyncio.Lock()
        total_dates = len(dates)
        
        # 复用 ControlMongodb 实例
        unique_keys = self._get_unique_keys()
        extra_fields = self._get_extra_fields()
        control_db = ControlMongodb(self.collection, unique_keys, self.current_user)
        
        async def process_date(date: str):
            """处理单个日期"""
            nonlocal processed, failed, success_count, total_inserted, empty_count
            
            async with semaphore:
                try:
                    # 调用 provider 获取数据
                    try:
                        df = await asyncio.wait_for(
                            asyncio.get_event_loop().run_in_executor(
                                None,
                                lambda d=date: self.provider.fetch_data(date=d)
                            ),
                            timeout=self.batch_task_timeout
                        )
                    except asyncio.TimeoutError:
                        logger.warning(f"[{self.collection_name}] 日期 {date} 超时")
                        raise TimeoutError(f"获取 {date} 数据超时")
                    
                    if df is not None and not df.empty:
                        # 保存数据
                        result = await control_db.save_dataframe_to_collection(
                            df, extra_fields=extra_fields
                        )
                        
                        inserted_count = result.get("inserted", 0) + result.get("updated", 0)
                        
                        async with lock:
                            total_inserted += inserted_count
                            success_count += 1
                        
                        logger.debug(f"[{self.collection_name}] 日期 {date} 保存完成: {inserted_count} 条")
                    else:
                        # 某些日期可能没有数据（非交易日等）
                        async with lock:
                            empty_count += 1
                        logger.debug(f"[{self.collection_name}] 日期 {date} 无数据")
                    
                    async with lock:
                        processed += 1
                        
                except Exception as e:
                    logger.warning(f"[{self.collection_name}] 日期 {date} 处理失败: {e}")
                    async with lock:
                        failed += 1
                        processed += 1
                
                # 更新进度
                async with lock:
                    current_processed = processed
                
                if task_manager and task_id and current_processed % 10 == 0:
                    progress = 10 + int((current_processed / total_dates) * 85)
                    task_manager.update_progress(
                        task_id, progress, 100,
                        f"已处理 {current_processed}/{total_dates} 个日期，"
                        f"成功 {success_count}，失败 {failed}，无数据 {empty_count}"
                    )
        
        # 并发执行所有日期的任务
        await asyncio.gather(*[process_date(date) for date in dates], return_exceptions=True)
        
        # 完成任务
        message = (
            f"批量更新完成：共处理 {total_dates} 个日期，"
            f"成功 {success_count}，失败 {failed}，无数据 {empty_count}，"
            f"共保存 {total_inserted} 条数据"
        )
        logger.info(f"[{self.collection_name}] {message}")
        
        if task_manager and task_id:
            task_manager.update_progress(task_id, 100, 100, message)
            task_manager.complete_task(
                task_id,
                result={"inserted": total_inserted, "success": success_count, "failed": failed},
                message=message
            )
        
        return {
            "success": True,
            "message": message,
            "inserted": total_inserted,
            "success_count": success_count,
            "failed": failed,
            "empty_count": empty_count
        }
