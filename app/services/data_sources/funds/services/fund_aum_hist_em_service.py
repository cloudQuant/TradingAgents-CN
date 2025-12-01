"""
基金规模历史-东财服务（重构版：继承BaseService，需要年份参数）
"""
from typing import Optional, Dict, Any, List, Set, Tuple
from datetime import datetime
import logging

from app.services.data_sources.base_service import BaseService
from app.services.data_sources.funds.providers.fund_aum_hist_em_provider import FundAumHistEmProvider
from app.services.database.control_mongodb import ControlMongodb

logger = logging.getLogger(__name__)


class FundAumHistEmService(BaseService):
    """基金规模历史-东财服务（需要年份参数）"""
    
    # ===== 必须定义的属性 =====
    collection_name = "fund_aum_hist_em"
    provider_class = FundAumHistEmProvider
    
    # ===== 可选配置 =====
    time_field = "更新时间"  # 时间字段名
    
    # 批量更新配置
    batch_source_collection = None  # 不需要从其他集合获取代码
    batch_source_field = None
    batch_years_range = (2001, None)  # 年份范围：2001年到今年
    batch_use_year = True  # 需要年份参数
    batch_concurrency = 3  # 默认并发数
    batch_progress_interval = 100  # 进度更新间隔
    
    # 增量更新检查字段（用于检查已存在的数据）
    # 注意：此接口每个年份返回所有基金公司的数据，所以只需要检查年份即可
    incremental_check_fields = ["年份"]
    
    # 唯一键配置
    unique_keys = ["基金公司", "年份"]
    
    # 额外的元数据字段
    extra_metadata = {
        "数据源": "akshare",
        "接口名称": "fund_aum_hist_em",
    }
    
    async def update_single_data(self, **kwargs) -> Dict[str, Any]:
        """
        更新单条数据（需要 year 参数）
        
        重写基类方法以保持原有的参数验证逻辑
        """
        try:
            self.logger.info(f"[{self.collection_name}] update_single_data 收到参数: {kwargs}")
            
            # 参数解析：支持多种参数名
            year = kwargs.get("year") or kwargs.get("date")
            
            self.logger.info(f"[{self.collection_name}] 解析参数: year={year}")
            
            # 参数验证
            if not year:
                return {
                    "success": False,
                    "message": "缺少必须参数: year（请提供年份，如 2024）",
                    "inserted": 0,
                }
            
            # 调用 provider 获取数据
            df = self.provider.fetch_data(year=year)
            
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
    
    async def _get_tasks_to_process(
        self, 
        codes: List[str] = None, 
        years: List[str] = None
    ) -> List[Tuple]:
        """
        获取待处理的任务列表（增量更新）
        
        重写基类方法，因为此接口不需要基金代码，只需要年份
        
        Args:
            codes: 基金代码列表（此接口不需要，忽略）
            years: 年份列表，如果为None则自动生成（从2001年开始）
            
        Returns:
            待处理的任务列表，格式：[(year,), ...]
        """
        # 如果没有提供年份列表，自动生成（从2001年开始）
        if years is None:
            years = self._get_years_range(None)
        
        # 如果没有配置增量检查，返回所有年份
        if not self.incremental_check_fields:
            return [(year,) for year in years]
        
        # 获取已存在的组合
        existing = await self._get_existing_combinations()
        
        # 过滤出需要处理的任务
        # 注意：existing 中的元组是字符串格式，需要确保格式一致
        tasks = [
            (str(year),) 
            for year in years 
            if (str(year),) not in existing
        ]
        
        logger.info(
            f"[{self.collection_name}] 总年份数: {len(years)}, "
            f"已存在: {len(existing)}, 待处理: {len(tasks)}"
        )
        
        return tasks
    
    def get_batch_params(self, *args) -> Dict[str, Any]:
        """
        构建批量任务的参数
        
        重写基类方法以匹配 provider 的参数格式
        
        Args:
            args[0]: 年份
        """
        if len(args) >= 1 and args[0]:
            year = args[0]
            return {"year": year}
        raise ValueError(f"get_batch_params 缺少必需的参数，需要年份，args={args}")
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """
        批量更新数据
        
        生成年份列表（从2001年开始），然后遍历所有年份进行批量更新。
        """
        try:
            from app.utils.task_manager import get_task_manager
            task_manager = get_task_manager() if task_id else None
            
            # 获取并发数
            concurrency = int(kwargs.get("concurrency", self.batch_concurrency))
            
            # 1. 生成年份列表（从2001年开始）
            if task_manager and task_id:
                task_manager.update_progress(
                    task_id, 0, 100, 
                    "正在生成年份列表..."
                )
            
            years = self._get_years_range(kwargs.get("year"))
            logger.info(f"[{self.collection_name}] 生成年份列表，共 {len(years)} 个年份")
            
            # 2. 获取待处理的任务列表（增量更新）
            tasks = await self._get_tasks_to_process(years=years)
            
            if not tasks:
                message = "所有年份的数据已存在，无需更新"
                if task_manager and task_id:
                    task_manager.complete_task(task_id, message)
                return {
                    "success": True,
                    "message": message,
                    "inserted": 0,
                    "skipped_count": len(years),
                }
            
            # 3. 执行批量更新
            if task_manager and task_id:
                task_manager.update_progress(
                    task_id, 10, 100, 
                    f"需要处理 {len(tasks)} 个年份的数据..."
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
