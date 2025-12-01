"""
基金持仓变动-东财服务（重构版：继承BaseService）
"""
from typing import Optional, Dict, Any, List, Set, Tuple
from datetime import datetime
import logging

from app.services.data_sources.base_service import BaseService
from app.services.data_sources.funds.providers.fund_portfolio_change_em_provider import FundPortfolioChangeEmProvider
from app.services.database.control_mongodb import ControlMongodb
from app.utils.task_manager import get_task_manager

logger = logging.getLogger(__name__)


class FundPortfolioChangeEmService(BaseService):
    """基金持仓变动-东财服务"""
    
    # ===== 必须定义的属性 =====
    collection_name = "fund_portfolio_change_em"
    provider_class = FundPortfolioChangeEmProvider
    
    # ===== 可选配置 =====
    time_field = "scraped_at"  # 时间字段名
    
    # 批量更新配置
    batch_source_collection = "fund_name_em"  # 从哪个集合获取基金代码列表
    batch_source_field = "基金代码"  # 从源集合获取的字段名
    batch_years_range = (2010, None)  # 年份范围：2010年到今年（但批量更新时year必填）
    batch_use_year = True  # 需要年份参数
    batch_concurrency = 3  # 默认并发数
    batch_progress_interval = 100  # 进度更新间隔
    
    # 增量更新检查字段（用于检查已存在的数据）
    # 改为检查"年份"字段，如果存在该年份就不更新
    incremental_check_fields = ["基金代码", "年份", "指标"]
    
    # 唯一键配置
    unique_keys = ["基金代码", "指标", "季度", "股票代码"]
    
    # 额外的元数据字段
    extra_metadata = {
        "数据源": "akshare",
        "接口名称": "fund_portfolio_change_em",
    }
    
    def __init__(self, db=None, current_user=None):
        """初始化服务，添加 indicator 实例变量"""
        super().__init__(db=db, current_user=current_user)
        self._batch_indicator = "累计买入"  # 批量更新时的默认指标
    
    async def update_single_data(self, **kwargs) -> Dict[str, Any]:
        """
        更新单条数据（需要 fund_code 和 year 参数）
        
        重写基类方法以保持原有的参数验证逻辑
        """
        try:
            self.logger.info(f"[{self.collection_name}] update_single_data 收到参数: {kwargs}")
            
            # 参数解析：支持多种参数名
            fund_code = kwargs.get("fund_code") or kwargs.get("symbol") or kwargs.get("code")
            year = kwargs.get("year") or kwargs.get("date")
            indicator = kwargs.get("indicator", "累计买入")  # 默认值为"累计买入"
            
            self.logger.info(f"[{self.collection_name}] 解析参数: fund_code={fund_code}, year={year}, indicator={indicator}")
            
            # 参数验证
            if not fund_code:
                return {
                    "success": False,
                    "message": "缺少必须参数: fund_code（单条更新需要提供基金代码，如需批量更新请使用批量更新功能）",
                    "inserted": 0,
                }
            if not year:
                return {
                    "success": False,
                    "message": "缺少必须参数: year（请提供年份，如 2024）",
                    "inserted": 0,
                }
            
            # 调用 provider 获取数据
            df = self.provider.fetch_data(fund_code=fund_code, year=year, indicator=indicator)
            
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
    
    async def update_batch_data(self, task_id: str = None, **kwargs) -> Dict[str, Any]:
        """
        批量更新基金持仓变动数据
        
        重写基类方法以支持 year 参数必填的特殊逻辑
        
        Args:
            task_id: 任务ID，用于更新进度
            year: 年份参数（必填）
            indicator: 指标类型（可选，默认"累计买入"）
            concurrency: 并发数（默认3）
        """
        try:
            task_manager = get_task_manager() if task_id else None
            year = kwargs.get("year")
            indicator = kwargs.get("indicator", "累计买入")  # 默认值为"累计买入"
            concurrency = int(kwargs.get("concurrency", self.batch_concurrency))
            
            # 年份必填（与基类的默认行为不同）
            if not year:
                if task_manager and task_id:
                    task_manager.fail_task(task_id, "缺少必须参数: year（批量更新需要指定年份）")
                return {
                    "success": False,
                    "message": "缺少必须参数: year（批量更新需要指定年份）",
                    "inserted": 0,
                }
            
            # 将 indicator 保存到实例变量中，以便在 get_batch_params 中使用
            self._batch_indicator = indicator
            
            # 从 kwargs 中移除已处理的参数，避免重复传递
            filtered_kwargs = {k: v for k, v in kwargs.items() if k not in ['year', 'indicator', 'concurrency']}
            
            # 调用基类的批量更新方法，但先验证年份参数
            result = await super().update_batch_data(task_id=task_id, year=year, concurrency=concurrency, **filtered_kwargs)
            
            # 重置 indicator
            self._batch_indicator = "累计买入"
            
            return result
            
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
    
    def get_batch_params(self, code: str, year: str) -> Dict[str, Any]:
        """
        构建批量任务的参数
        
        重写基类方法以匹配 provider 的参数格式
        
        Args:
            code: 基金代码
            year: 年份
        """
        params = {"fund_code": code, "year": year}
        # 使用实例变量中的 indicator（在 update_batch_data 中设置）
        params["indicator"] = getattr(self, "_batch_indicator", "累计买入")
        return params
