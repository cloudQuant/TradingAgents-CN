"""
基金持仓股票-东财服务（重构版：继承BaseService）
"""
from typing import Optional, Dict, Any, List, Set, Tuple
from datetime import datetime
import logging

from app.services.data_sources.base_service import BaseService
from app.services.data_sources.funds.providers.fund_portfolio_hold_em_provider import FundPortfolioHoldEmProvider
from app.services.database.control_mongodb import ControlMongodb

logger = logging.getLogger(__name__)


class FundPortfolioHoldEmService(BaseService):
    """基金持仓股票-东财服务"""
    
    # ===== 必须定义的属性 =====
    collection_name = "fund_portfolio_hold_em"
    provider_class = FundPortfolioHoldEmProvider
    
    # ===== 可选配置 =====
    time_field = "更新时间"  # 时间字段名
    
    # 批量更新配置
    batch_source_collection = "fund_name_em"  # 从哪个集合获取基金代码列表
    batch_source_field = "基金代码"  # 从源集合获取的字段名
    batch_years_range = (2010, None)  # 年份范围：2010年到今年
    batch_use_year = True  # 需要年份参数
    batch_concurrency = 3  # 默认并发数
    batch_progress_interval = 100  # 进度更新间隔
    
    # 增量更新检查字段（用于检查已存在的数据）
    # 注意：这里使用 ["基金代码", "季度"] 来检查，但实际检查逻辑需要从季度中提取年份
    incremental_check_fields = ["基金代码", "季度"]
    
    # 字段值提取器：从"季度"字段中提取年份
    # 季度格式如 "2024年1季度"，需要提取年份部分 "2024"
    incremental_field_extractor = {
        "季度": lambda q: q[:4] if len(q) >= 4 and q[:4].isdigit() else ""
    }
    
    # 唯一键配置（因为旧provider没有get_unique_keys方法）
    unique_keys = ["基金代码", "股票代码", "季度"]
    
    # 额外的元数据字段
    extra_metadata = {
        "数据源": "akshare",
        "接口名称": "fund_portfolio_hold_em",
    }
    
    
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
            
            self.logger.info(f"[{self.collection_name}] 解析参数: fund_code={fund_code}, year={year}")
            
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
            df = self.provider.fetch_data(fund_code=fund_code, year=year)
            
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
    
    def get_batch_params(self, code: str, year: str) -> Dict[str, Any]:
        """
        构建批量任务的参数
        
        重写基类方法以匹配 provider 的参数格式
        """
        return {"fund_code": code, "year": year}
