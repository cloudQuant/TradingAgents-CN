"""
基金持仓明细-雪球服务（重构版：继承BaseService，需要symbol和date参数）
"""
from typing import Dict, Any, List, Set, Tuple
from datetime import datetime
import logging

from app.services.data_sources.base_service import BaseService
from ..providers.fund_individual_detail_hold_xq_provider import FundIndividualDetailHoldXqProvider

logger = logging.getLogger(__name__)


class FundIndividualDetailHoldXqService(BaseService):
    """基金持仓明细-雪球服务（需要基金代码和季度日期参数）"""
    
    collection_name = "fund_individual_detail_hold_xq"
    provider_class = FundIndividualDetailHoldXqProvider
    
    # 批量更新配置：从 fund_name_em 获取基金代码列表
    batch_source_collection = "fund_name_em"
    batch_source_field = "基金代码"
    
    # 并发控制
    batch_concurrency = 3
    batch_progress_interval = 20
    
    # 增量更新：根据基金代码和季度日期检查是否已存在
    incremental_check_fields = ["基金代码", "季度日期"]
    
    # 唯一键配置（基金代码 + 季度日期 + 资产类别）
    unique_keys = ["基金代码", "季度日期", "资产类别"]
    
    # 额外的元数据字段
    extra_metadata = {
        "数据源": "akshare",
        "接口名称": "fund_individual_detail_hold_xq",
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
        codes: List[str], 
        dates: List[str] = None
    ) -> List[Tuple]:
        """
        获取待处理的任务列表（增量更新）
        
        检查当前数据集合中是否存在基金代码和日期组合，如果存在就不更新
        
        Args:
            codes: 基金代码列表
            dates: 季度日期列表，如果为None则自动生成（从2010年开始）
            
        Returns:
            待处理的任务列表，格式：[(code, date), ...]
        """
        # 如果没有提供日期列表，自动生成（从2010年开始）
        if dates is None:
            dates = self._get_quarter_dates(start_year=2010)
        
        # 如果没有配置增量检查，返回所有组合
        if not self.incremental_check_fields:
            return [(code, date) for code in codes for date in dates]
        
        # 获取已存在的组合
        existing = await self._get_existing_combinations()
        
        # 过滤出需要处理的任务
        # 注意：existing 中的元组是字符串格式，需要确保格式一致
        tasks = [
            (str(code), str(date)) 
            for code in codes 
            for date in dates 
            if (str(code), str(date)) not in existing
        ]
        
        logger.info(
            f"[{self.collection_name}] 总组合数: {len(codes) * len(dates)}, "
            f"已存在: {len(existing)}, 待处理: {len(tasks)}"
        )
        
        return tasks
    
    
    def get_batch_params(self, *args) -> Dict[str, Any]:
        """
        构建批量更新参数
        
        Args:
            args[0]: 基金代码
            args[1]: 季度日期
            
        Returns:
            provider 调用参数
        """
        if len(args) >= 2 and args[0] and args[1]:
            code = args[0]
            date = args[1]
            return {"symbol": code, "date": date}
        raise ValueError(f"get_batch_params 缺少必需的参数，需要基金代码和季度日期，args={args}")
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """
        批量更新数据
        
        从 fund_name_em 获取基金代码列表，生成季度日期列表（从2010年开始），
        然后遍历所有组合进行批量更新。
        """
        try:
            from app.utils.task_manager import get_task_manager
            task_manager = get_task_manager() if task_id else None
            
            # 获取并发数
            concurrency = int(kwargs.get("concurrency", self.batch_concurrency))
            
            # 1. 获取代码列表
            if task_manager and task_id:
                task_manager.update_progress(
                    task_id, 0, 100, 
                    f"正在从 {self.batch_source_collection} 获取代码列表..."
                )
            
            codes = await self._get_source_codes()
            
            if not codes:
                if task_manager and task_id:
                    task_manager.fail_task(
                        task_id, 
                        f"{self.batch_source_collection} 集合为空，请先更新相关数据"
                    )
                return {
                    "success": False,
                    "message": f"{self.batch_source_collection} 集合为空",
                    "inserted": 0,
                }
            
            self.logger.info(f"[{self.collection_name}] 从 {self.batch_source_collection} 获取到 {len(codes)} 个代码")
            
            # 2. 生成季度日期列表（从2010年开始）
            quarter_dates = self._get_quarter_dates(start_year=2010)
            self.logger.info(f"[{self.collection_name}] 生成 {len(quarter_dates)} 个季度日期")
            
            # 3. 生成待处理的任务列表（增量更新检查）
            if task_manager and task_id:
                task_manager.update_progress(task_id, 5, 100, "正在检查已有数据...")
            
            tasks_to_process = await self._get_tasks_to_process(codes, quarter_dates)
            
            if not tasks_to_process:
                if task_manager and task_id:
                    task_manager.update_progress(task_id, 100, 100, "所有数据已存在，无需更新")
                    task_manager.complete_task(task_id)
                return {
                    "success": True,
                    "message": "所有数据已存在，无需更新",
                    "inserted": 0,
                }
            
            total_tasks = len(tasks_to_process)
            self.logger.info(f"[{self.collection_name}] 需要处理 {total_tasks} 个任务")
            
            if task_manager and task_id:
                task_manager.update_progress(task_id, 10, 100, f"需要处理 {total_tasks} 个任务...")
            
            # 4. 并发执行
            return await self._execute_batch_tasks(
                tasks_to_process, 
                task_id, 
                task_manager, 
                concurrency
            )
            
        except Exception as e:
            self.logger.error(f"[{self.collection_name}] 批量更新失败: {e}", exc_info=True)
            if task_manager and task_id:
                task_manager.fail_task(task_id, f"批量更新失败: {str(e)}")
            return {
                "success": False,
                "message": f"批量更新失败: {str(e)}",
                "inserted": 0,
            }
