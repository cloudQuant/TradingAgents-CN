"""
基金拆分-东财服务（重构版：继承BaseService）
"""
from typing import Optional, Dict, Any, List, Set
from datetime import datetime
import logging
import asyncio

from app.services.data_sources.base_service import BaseService
from app.services.data_sources.funds.providers.fund_cf_em_provider import FundCfEmProvider
from app.services.database.control_mongodb import ControlMongodb
from app.utils.task_manager import get_task_manager

logger = logging.getLogger(__name__)


class FundCfEmService(BaseService):
    """基金拆分-东财服务"""
    
    # ===== 必须定义的属性 =====
    collection_name = "fund_cf_em"
    provider_class = FundCfEmProvider
    
    # ===== 可选配置 =====
    time_field = "scraped_at"
    
    # 批量更新配置：按年份批量更新
    batch_years_range = (2005, None)  # 年份范围：2005年到今年
    batch_concurrency = 3
    batch_progress_interval = 10
    
    # 增量更新检查字段（用于检查已存在的年份）
    incremental_check_fields = ["年份"]
    
    # 唯一键配置
    unique_keys = ["基金代码", "拆分折算日", "年份"]
    
    # 额外的元数据字段
    extra_metadata = {
        "数据源": "akshare",
        "接口名称": "fund_cf_em",
    }
    
    async def update_single_data(self, **kwargs) -> Dict[str, Any]:
        """更新单条数据（需要 year 参数）"""
        try:
            self.logger.info(f"[{self.collection_name}] update_single_data 收到参数: {kwargs}")
            year = kwargs.get("year") or kwargs.get("date")
            self.logger.info(f"[{self.collection_name}] 解析参数: year={year}")
            
            # 参数验证
            if not year:
                return {
                    "success": False,
                    "message": "缺少必须参数: year（请提供年份，如 2020）",
                    "inserted": 0,
                }
            
            self.logger.info(f"[{self.collection_name}] 调用 provider.fetch_data(year={year})")
            df = self.provider.fetch_data(year=year)
            
            if df is None or df.empty:
                self.logger.warning(f"[{self.collection_name}] provider 返回空数据")
                return {
                    "success": True,
                    "message": "No data available",
                    "inserted": 0,
                }
            
            # 使用 ControlMongodb 处理数据去重
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
            
        except Exception as e:
            self.logger.error(f"[{self.collection_name}] update_single_data 发生错误: {str(e)}")
            return {
                "success": False,
                "message": str(e),
                "inserted": 0,
            }
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """
        批量更新基金拆分数据（按年份遍历）
        
        Args:
            task_id: 任务ID，用于更新进度
            concurrency: 并发数（默认3）
        """
        try:
            task_manager = get_task_manager() if task_id else None
            concurrency = int(kwargs.get("concurrency", self.batch_concurrency))
            
            if task_manager and task_id:
                task_manager.update_progress(task_id, 0, 100, "正在准备年份列表...")
            
            # 1. 生成年份范围
            start_year, end_year = self.batch_years_range
            if end_year is None:
                end_year = datetime.now().year
            years = [str(y) for y in range(start_year, end_year + 1)]
            
            self.logger.info(f"[{self.collection_name}] 年份范围: {years[0]} - {years[-1]}")
            
            # 2. 获取已存在的年份（增量更新）
            if task_manager and task_id:
                task_manager.update_progress(task_id, 5, 100, "正在检查已有数据，避免重复获取...")
            
            existing_years: Set[str] = set()
            existing_cursor = self.collection.find({}, {"年份": 1})
            async for doc in existing_cursor:
                y = doc.get("年份")
                if y:
                    existing_years.add(str(y))
            
            self.logger.info(f"[{self.collection_name}] 已存在 {len(existing_years)} 个年份的数据")
            
            # 3. 生成待更新的年份（排除已存在的）
            years_to_update = [y for y in years if y not in existing_years]
            
            if not years_to_update:
                if task_manager and task_id:
                    task_manager.update_progress(task_id, 100, 100, "所有年份数据已存在，无需更新")
                    task_manager.complete_task(task_id)
                return {
                    "success": True,
                    "message": "所有年份数据已存在，无需更新",
                    "inserted": 0,
                }
            
            total_years = len(years_to_update)
            self.logger.info(f"[{self.collection_name}] 需要更新 {total_years} 个年份")
            
            if task_manager and task_id:
                task_manager.update_progress(task_id, 10, 100, f"需要更新 {total_years} 个年份，开始并发获取...")
            
            # 4. 使用基类的批量任务执行方法
            tasks = [(year,) for year in years_to_update]
            return await self._execute_batch_tasks(tasks, task_id, task_manager, concurrency)
            
        except Exception as e:
            self.logger.error(f"[{self.collection_name}] 批量更新失败: {e}", exc_info=True)
            task_manager = get_task_manager() if task_id else None
            if task_manager and task_id:
                task_manager.fail_task(task_id, str(e))
            return {
                "success": False,
                "message": str(e),
                "inserted": 0,
            }
    
    def get_batch_params(self, year: str) -> Dict[str, Any]:
        """
        构建批量任务的参数
        
        重写基类方法以匹配 provider 的参数格式（只需要year参数）
        """
        return {"year": year}
