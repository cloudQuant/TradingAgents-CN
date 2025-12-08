"""
日期增量更新服务基类

为需要日期参数的期货数据集合提供通用的增量更新功能
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging
import asyncio
from abc import ABC

from app.services.data_sources.base_service import BaseService
from app.services.database.control_mongodb import ControlMongodb
from app.utils.task_manager import get_task_manager

logger = logging.getLogger(__name__)


class DateIncrementalService(BaseService, ABC):
    """
    日期增量更新服务基类
    
    子类需要定义：
    - collection_name: 集合名称
    - provider_class: Provider类
    - time_field: 日期字段名（默认"日期"）
    - unique_keys: 唯一键列表
    - DEFAULT_START_DATE: 默认开始日期（默认"20100101"）
    """
    
    # 默认配置
    time_field = "日期"
    DEFAULT_START_DATE = "20100101"
    
    # 日期格式：YYYYMMDD 或 YYYYMM
    DATE_FORMAT = "%Y%m%d"  # 子类可覆盖为 "%Y%m" 
    
    # 是否跳过周末
    SKIP_WEEKENDS = True
    
    # API调用间隔（秒）
    API_DELAY = 0.1
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """
        批量更新（增量更新）
        
        从数据库最大日期开始，逐日/逐月获取数据直到今天
        """
        task_manager = get_task_manager() if task_id else None
        
        try:
            # 获取开始日期
            start_date_str = kwargs.get("start_date")
            if not start_date_str:
                start_date_str = await self._get_max_date()
            
            # 解析日期
            try:
                if len(self.DATE_FORMAT) == 6:  # YYYYMM
                    start_date = datetime.strptime(start_date_str[:6], "%Y%m")
                else:
                    start_date = datetime.strptime(start_date_str[:8], "%Y%m%d")
            except ValueError:
                start_date = datetime.strptime(self.DEFAULT_START_DATE[:8], "%Y%m%d")
            
            # 从最大日期的下一天/下一月开始
            if self.DATE_FORMAT == "%Y%m":
                # 月份格式，加一个月
                if start_date.month == 12:
                    start_date = start_date.replace(year=start_date.year + 1, month=1)
                else:
                    start_date = start_date.replace(month=start_date.month + 1)
            else:
                start_date = start_date + timedelta(days=1)
            
            end_date = datetime.now()
            
            # 生成日期列表
            dates_to_process = self._generate_date_list(start_date, end_date)
            
            if not dates_to_process:
                message = f"数据已是最新，无需更新（最大日期：{start_date_str}）"
                if task_manager and task_id:
                    task_manager.update_progress(task_id, 100, 100, message)
                    task_manager.complete_task(task_id, message=message)
                return {"success": True, "message": message, "inserted": 0}
            
            total_dates = len(dates_to_process)
            self.logger.info(f"[{self.collection_name}] 需要更新 {total_dates} 个日期")
            
            if task_manager and task_id:
                task_manager.update_progress(task_id, 5, 100, f"需要更新 {total_dates} 个日期")
            
            # 逐日获取数据
            total_inserted = 0
            success_count = 0
            failed_count = 0
            
            for i, date_str in enumerate(dates_to_process):
                try:
                    # 获取数据
                    df = await asyncio.get_event_loop().run_in_executor(
                        None,
                        lambda d=date_str: self.provider.fetch_data(date=d)
                    )
                    
                    if df is not None and not df.empty:
                        # 保存数据
                        unique_keys = self._get_unique_keys()
                        control_db = ControlMongodb(self.collection, unique_keys, self.current_user)
                        result = await control_db.save_dataframe_to_collection(df)
                        inserted = result.get("inserted", 0) + result.get("updated", 0)
                        total_inserted += inserted
                        success_count += 1
                        self.logger.debug(f"[{self.collection_name}] {date_str}: 保存 {inserted} 条")
                    else:
                        self.logger.debug(f"[{self.collection_name}] {date_str}: 无数据（可能是非交易日）")
                    
                except Exception as e:
                    failed_count += 1
                    self.logger.warning(f"[{self.collection_name}] {date_str} 获取失败: {e}")
                
                # 更新进度
                if task_manager and task_id:
                    progress = 5 + int((i + 1) / total_dates * 90)
                    task_manager.update_progress(
                        task_id, progress, 100,
                        f"已处理 {i + 1}/{total_dates}，成功 {success_count}，失败 {failed_count}"
                    )
                
                # 控制API调用频率
                await asyncio.sleep(self.API_DELAY)
            
            message = f"增量更新完成：处理 {total_dates} 个日期，成功 {success_count}，失败 {failed_count}，保存 {total_inserted} 条"
            
            if task_manager and task_id:
                task_manager.update_progress(task_id, 100, 100, message)
                task_manager.complete_task(task_id, result={"inserted": total_inserted}, message=message)
            
            return {"success": True, "message": message, "inserted": total_inserted}
            
        except Exception as e:
            self.logger.error(f"[{self.collection_name}] 批量更新失败: {e}", exc_info=True)
            if task_manager and task_id:
                task_manager.fail_task(task_id, str(e))
            return {"success": False, "message": str(e), "inserted": 0}
    
    def _generate_date_list(self, start_date: datetime, end_date: datetime) -> List[str]:
        """生成日期列表"""
        dates = []
        current = start_date
        
        if self.DATE_FORMAT == "%Y%m":
            # 月份格式
            while current <= end_date:
                dates.append(current.strftime("%Y%m"))
                if current.month == 12:
                    current = current.replace(year=current.year + 1, month=1)
                else:
                    current = current.replace(month=current.month + 1)
        else:
            # 日期格式
            while current <= end_date:
                if not self.SKIP_WEEKENDS or current.weekday() < 5:
                    dates.append(current.strftime("%Y%m%d"))
                current += timedelta(days=1)
        
        return dates
    
    async def _get_max_date(self) -> str:
        """获取数据库中的最大日期"""
        try:
            pipeline = [
                {"$group": {"_id": None, "max_date": {"$max": f"${self.time_field}"}}}
            ]
            cursor = self.collection.aggregate(pipeline)
            result = await cursor.to_list(length=1)
            
            if result and result[0].get("max_date"):
                max_date = result[0]["max_date"]
                if isinstance(max_date, datetime):
                    return max_date.strftime(self.DATE_FORMAT)
                elif isinstance(max_date, str):
                    # 清理日期字符串
                    clean_date = max_date.replace("-", "").replace("/", "")
                    if self.DATE_FORMAT == "%Y%m":
                        return clean_date[:6]
                    return clean_date[:8]
            
            return self.DEFAULT_START_DATE
            
        except Exception as e:
            self.logger.warning(f"[{self.collection_name}] 获取最大日期失败: {e}")
            return self.DEFAULT_START_DATE
