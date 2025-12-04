"""
资产负债表服务

同花顺-财务指标-资产负债表
接口: stock_financial_debt_ths
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_financial_debt_ths_provider import StockFinancialDebtThsProvider


class StockFinancialDebtThsService(BaseService):
    """资产负债表服务"""
    
    collection_name = "stock_financial_debt_ths"
    provider_class = StockFinancialDebtThsProvider
    
    # 时间字段名
    time_field = "更新时间"
