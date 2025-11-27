"""
理财型基金历史行情-东财服务（重构版：继承BaseService）
"""
from typing import Optional, Dict, Any, List, Set
from datetime import datetime
import logging

from app.services.data_sources.base_service import BaseService
from app.services.data_sources.funds.providers.fund_financial_fund_info_em_provider import FundFinancialFundInfoEmProvider
from app.services.database.control_mongodb import ControlMongodb

logger = logging.getLogger(__name__)


class FundFinancialFundInfoEmService(BaseService):
    """理财型基金历史行情-东财服务"""
    
    # ===== 必须定义的属性 =====
    collection_name = "fund_financial_fund_info_em"
    provider_class = FundFinancialFundInfoEmProvider
    
    # ===== 可选配置 =====
    time_field = "scraped_at"
    
    # 批量更新配置：从fund_financial_fund_daily_em获取基金代码列表
    batch_source_collection = "fund_financial_fund_daily_em"
    batch_source_field = "基金代码"
    batch_concurrency = 3
    batch_progress_interval = 50
    
    # 增量更新检查字段
    incremental_check_fields = ["基金代码"]
    
    # 唯一键配置
    unique_keys = ["基金代码", "净值日期"]
    
    # 额外的元数据字段
    extra_metadata = {
        "数据源": "akshare",
        "接口名称": "fund_financial_fund_info_em",
    }
    
    async def update_single_data(self, **kwargs) -> Dict[str, Any]:
        """更新单条数据（需要 fund_code 参数）"""
        try:
            self.logger.info(f"[{self.collection_name}] update_single_data 收到参数: {kwargs}")
            fund_code = kwargs.get("fund_code") or kwargs.get("fund") or kwargs.get("code")
            self.logger.info(f"[{self.collection_name}] 解析参数: fund_code={fund_code}")
            
            # 参数验证
            if not fund_code:
                return {
                    "success": False,
                    "message": "缺少必须参数: fund_code（单条更新需要提供基金代码，如需批量更新请使用批量更新功能）",
                    "inserted": 0,
                }
            
            self.logger.info(f"[{self.collection_name}] 调用 provider.fetch_data(fund_code={fund_code})")
            df = self.provider.fetch_data(fund_code=fund_code)
            
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
    
    def get_batch_params(self, code: str) -> Dict[str, Any]:
        """
        构建批量任务的参数
        
        重写基类方法以匹配 provider 的参数格式（只需要fund_code参数）
        """
        return {"fund_code": code}
