"""
基金评级-上海证券-东财服务（重构版：继承BaseService，需要季度日期参数）
"""
from typing import Dict, Any, List, Set, Tuple
from datetime import datetime
import logging

from app.services.data_sources.base_service import BaseService
from app.services.data_sources.funds.providers.fund_rating_sh_em_provider import FundRatingShEmProvider

logger = logging.getLogger(__name__)


class FundRatingShEmService(BaseService):
    """基金评级-上海证券-东财服务（需要季度日期参数）"""
    
    collection_name = "fund_rating_sh_em"
    provider_class = FundRatingShEmProvider
    
    # 批量更新配置：不需要从其他集合获取代码，因为接口返回所有基金的数据
    # 但我们需要生成季度日期列表
    batch_source_collection = None  # 不需要从其他集合获取代码
    batch_source_field = None
    
    # 并发控制
    batch_concurrency = 3
    batch_progress_interval = 20
    
    # 增量更新：根据季度日期检查是否已存在
    incremental_check_fields = ["季度日期"]
    
    # 唯一键配置（代码 + 日期）
    unique_keys = ["代码", "日期"]
    
    # 额外的元数据字段
    extra_metadata = {
        "数据源": "akshare",
        "接口名称": "fund_rating_sh_em",
    }
    
    def _get_quarter_dates(self, start_year: int = 2010) -> List[str]:
        """
        生成季度日期列表（从指定年份开始到当前年份）
        
        季度末日期：
        - Q1: 3月31日
        - Q2: 6月30日
        - Q3: 9月30日
        - Q4: 12月31日
        
        Args:
            start_year: 起始年份，默认2010
            
        Returns:
            季度日期列表，格式：["2010-03-31", "2010-06-30", ...]
        """
        current_year = datetime.now().year
        quarter_dates = []
        
        for year in range(start_year, current_year + 1):
            quarter_dates.extend([
                f"{year}-03-31",  # Q1
                f"{year}-06-30",  # Q2
                f"{year}-09-30",  # Q3
                f"{year}-12-31",  # Q4
            ])
        
        return quarter_dates
    
    async def _get_tasks_to_process(
        self, 
        codes: List[str] = None, 
        dates: List[str] = None
    ) -> List[Tuple]:
        """
        获取待处理的任务列表（增量更新）
        
        检查当前数据集合中是否存在季度日期，如果存在就不更新
        
        Args:
            codes: 基金代码列表（此接口不需要，因为接口返回所有基金的数据）
            dates: 季度日期列表，如果为None则自动生成（从2010年开始）
            
        Returns:
            待处理的任务列表，格式：[(date,), ...]
        """
        # 如果没有提供日期列表，自动生成（从2010年开始）
        if dates is None:
            dates = self._get_quarter_dates(start_year=2010)
        
        # 如果没有配置增量检查，返回所有日期
        if not self.incremental_check_fields:
            return [(date,) for date in dates]
        
        # 获取已存在的组合
        existing = await self._get_existing_combinations()
        
        # 过滤出需要处理的任务
        # 注意：existing 中的元组是字符串格式，需要确保格式一致
        tasks = [
            (str(date),) 
            for date in dates 
            if (str(date),) not in existing
        ]
        
        logger.info(
            f"[{self.collection_name}] 总日期数: {len(dates)}, "
            f"已存在: {len(existing)}, 待处理: {len(tasks)}"
        )
        
        return tasks
    
    async def update_single_data(self, **kwargs) -> Dict[str, Any]:
        """
        更新单条数据（需要 quarter_date 参数）
        
        重写基类方法以保持原有的参数验证逻辑
        """
        try:
            self.logger.info(f"[{self.collection_name}] update_single_data 收到参数: {kwargs}")
            
            # 参数解析：支持多种参数名
            quarter_date = kwargs.get("quarter_date") or kwargs.get("date") or kwargs.get("qdate")
            
            self.logger.info(f"[{self.collection_name}] 解析参数: quarter_date={quarter_date}")
            
            # 参数验证
            if not quarter_date:
                return {
                    "success": False,
                    "message": "缺少必须参数: quarter_date（请提供季度日期，格式：YYYY-MM-DD，如 2024-03-31）",
                    "inserted": 0,
                }
            
            # 调用 provider 获取数据
            df = self.provider.fetch_data(quarter_date=quarter_date)
            
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
            args[0]: 季度日期
            
        Returns:
            provider 调用参数
        """
        if len(args) >= 1 and args[0]:
            date = args[0]
            return {"quarter_date": date}
        raise ValueError(f"get_batch_params 缺少必需的参数，需要季度日期，args={args}")
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """
        批量更新数据
        
        生成季度日期列表（从2010年Q1开始），然后遍历所有日期进行批量更新。
        """
        try:
            from app.utils.task_manager import get_task_manager
            task_manager = get_task_manager() if task_id else None
            
            # 获取并发数
            concurrency = int(kwargs.get("concurrency", self.batch_concurrency))
            
            # 1. 生成季度日期列表（从2010年Q1开始）
            if task_manager and task_id:
                task_manager.update_progress(
                    task_id, 0, 100, 
                    "正在生成季度日期列表..."
                )
            
            quarter_dates = self._get_quarter_dates(start_year=2010)
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
            from app.utils.task_manager import get_task_manager
            task_manager = get_task_manager() if task_id else None
            
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
