"""
基金报告行业配置-巨潮服务（重构版：继承BaseService，需要date参数）
"""
from typing import Dict, Any, List, Set, Tuple
from datetime import datetime
import logging

from app.services.data_sources.base_service import BaseService
from app.services.data_sources.funds.providers.fund_report_industry_allocation_cninfo_provider import FundReportIndustryAllocationCninfoProvider

logger = logging.getLogger(__name__)


class FundReportIndustryAllocationCninfoService(BaseService):
    """基金报告行业配置-巨潮服务（需要日期参数）"""
    
    collection_name = "fund_report_industry_allocation_cninfo"
    provider_class = FundReportIndustryAllocationCninfoProvider
    
    # 批量更新配置：不需要从其他集合获取代码，因为接口返回所有行业的数据
    # 但我们需要生成季度日期列表
    batch_source_collection = None  # 不需要从其他集合获取代码
    batch_source_field = None
    
    # 并发控制
    batch_concurrency = 3
    batch_progress_interval = 20
    
    # 增量更新：根据日期和行业编码检查是否已存在
    incremental_check_fields = ["日期", "行业编码"]
    
    # 唯一键配置（行业编码 + 日期）
    unique_keys = ["行业编码", "日期"]
    
    # 额外的元数据字段
    extra_metadata = {
        "数据源": "akshare",
        "接口名称": "fund_report_industry_allocation_cninfo",
    }
    
    def _get_quarter_dates(self, start_year: int = 2017) -> List[str]:
        """
        生成季度日期列表（从指定年份开始到当前年份）
        
        季度末日期格式：YYYYMMDD
        - Q1: 0331
        - Q2: 0630
        - Q3: 0930
        - Q4: 1231
        
        Args:
            start_year: 起始年份，默认2017
            
        Returns:
            季度日期列表，格式：["20170331", "20170630", ...]
        """
        current_year = datetime.now().year
        quarter_dates = []
        
        for year in range(start_year, current_year + 1):
            quarter_dates.extend([
                f"{year}0331",  # Q1
                f"{year}0630",  # Q2
                f"{year}0930",  # Q3
                f"{year}1231",  # Q4
            ])
        
        return quarter_dates
    
    async def _get_tasks_to_process(
        self, 
        codes: List[str] = None, 
        dates: List[str] = None
    ) -> List[Tuple]:
        """
        获取待处理的任务列表（增量更新）
        
        检查当前数据集合中是否存在日期和行业编码的组合，如果存在就不更新
        
        Args:
            codes: 行业编码列表（此接口不需要，因为接口返回所有行业的数据）
            dates: 季度日期列表，如果为None则自动生成（从2017年开始）
            
        Returns:
            待处理的任务列表，格式：[(date,), ...]
        """
        # 如果没有提供日期列表，自动生成（从2017年开始）
        if dates is None:
            dates = self._get_quarter_dates(start_year=2017)
        
        # 如果没有配置增量检查，返回所有日期
        if not self.incremental_check_fields:
            return [(date,) for date in dates]
        
        # 获取已存在的组合
        existing = await self._get_existing_combinations()
        
        # 过滤出需要处理的任务
        # 注意：existing 中的元组是 (日期, 行业编码) 格式，日期格式是 YYYY-MM-DD
        # 我们需要检查是否存在该日期的任何数据
        # 为了简化，我们检查是否存在该日期的数据（通过检查日期是否在existing的第一列中）
        existing_dates = {item[0] for item in existing if len(item) > 0}
        
        # 将 YYYYMMDD 格式转换为 YYYY-MM-DD 格式进行比较
        tasks = []
        for date in dates:
            date_str = str(date)
            # 如果是 YYYYMMDD 格式，转换为 YYYY-MM-DD
            if len(date_str) == 8 and date_str.isdigit():
                date_formatted = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
            else:
                date_formatted = date_str
            
            # 如果该日期不存在，添加到任务列表
            if date_formatted not in existing_dates:
                tasks.append((date_str,))
        
        logger.info(
            f"[{self.collection_name}] 总日期数: {len(dates)}, "
            f"已存在日期数: {len(existing_dates)}, 待处理: {len(tasks)}"
        )
        
        return tasks
    
    async def update_single_data(self, **kwargs) -> Dict[str, Any]:
        """
        更新单条数据（需要 date 参数）
        
        重写基类方法以保持原有的参数验证逻辑
        """
        try:
            self.logger.info(f"[{self.collection_name}] update_single_data 收到参数: {kwargs}")
            
            # 参数解析：支持多种参数名
            date = kwargs.get("date") or kwargs.get("quarter_date") or kwargs.get("qdate")
            
            self.logger.info(f"[{self.collection_name}] 解析参数: date={date}")
            
            # 参数验证
            if not date:
                return {
                    "success": False,
                    "message": "缺少必须参数: date（请提供季度日期，格式：YYYY-MM-DD 或 YYYYMMDD，如 2021-06-30 或 20210630）",
                    "inserted": 0,
                }
            
            # 调用 provider 获取数据
            df = self.provider.fetch_data(date=date)
            
            if df is None or df.empty:
                self.logger.warning(f"[{self.collection_name}] provider 返回空数据")
                return {
                    "success": True,
                    "message": "No data available",
                    "inserted": 0,
                }
            
            # 使用 ControlMongodb 保存数据（使用基类的自动检测方法）
            unique_keys = self._get_unique_keys()
            extra_fields = self._get_extra_fields()
            
            from app.services.database.control_mongodb import ControlMongodb
            control_db = ControlMongodb(self.collection, unique_keys)
            result = await control_db.save_dataframe_to_collection(df, extra_fields=extra_fields)
            
            return {
                "success": result["success"],
                "message": result["message"],
                "inserted": result.get("inserted", 0) + result.get("updated", 0),
                "details": result,
            }
            
        except ValueError as e:
            # 参数验证错误
            return {
                "success": False,
                "message": str(e),
                "inserted": 0,
            }
        except Exception as e:
            self.logger.error(f"[{self.collection_name}] update_single_data 发生错误: {str(e)}")
            return {
                "success": False,
                "message": str(e),
                "inserted": 0,
            }
    
    def get_batch_params(self, *args) -> Dict[str, Any]:
        """
        构建批量任务的参数
        
        Args:
            args[0]: 季度日期（YYYYMMDD格式）
            
        Returns:
            provider 调用参数
        """
        if len(args) >= 1 and args[0]:
            date = args[0]
            return {"date": date}
        raise ValueError(f"get_batch_params 缺少必需的参数，需要季度日期，args={args}")
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """
        批量更新数据
        
        生成季度日期列表（从2017年Q1开始），然后遍历所有日期进行批量更新。
        """
        try:
            from app.utils.task_manager import get_task_manager
            task_manager = get_task_manager() if task_id else None
            
            # 获取并发数
            concurrency = int(kwargs.get("concurrency", self.batch_concurrency))
            
            # 1. 生成季度日期列表（从2017年Q1开始）
            if task_manager and task_id:
                task_manager.update_progress(
                    task_id, 0, 100, 
                    "正在生成季度日期列表..."
                )
            
            quarter_dates = self._get_quarter_dates(start_year=2017)
            logger.info(f"[{self.collection_name}] 生成季度日期列表，共 {len(quarter_dates)} 个日期")
            
            # 2. 获取待处理的任务列表（增量更新）
            tasks = await self._get_tasks_to_process(dates=quarter_dates)
            
            if not tasks:
                message = "所有季度日期的数据已存在，无需更新"
                if task_manager and task_id:
                    task_manager.complete_task(task_id, message)
                return {
                    "success": True,
                    "message": message,
                    "inserted": 0,
                    "skipped_count": len(quarter_dates),
                }
            
            # 3. 执行批量更新
            if task_manager and task_id:
                task_manager.update_progress(
                    task_id, 10, 100, 
                    f"需要处理 {len(tasks)} 个季度日期的数据..."
                )
            
            return await self._execute_batch_tasks(
                tasks=tasks,
                task_id=task_id,
                task_manager=task_manager,
                concurrency=concurrency
            )
            
        except Exception as e:
            self.logger.error(f"[{self.collection_name}] 批量更新失败: {e}", exc_info=True)
            from app.utils.task_manager import get_task_manager
            task_manager = get_task_manager() if task_id else None
            if task_manager and task_id:
                task_manager.fail_task(task_id, str(e))
            return {
                "success": False,
                "message": str(e),
                "inserted": 0,
            }
