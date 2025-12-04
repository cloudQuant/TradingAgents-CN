"""
现金流量表服务

同花顺-财务指标-现金流量表
接口: stock_financial_cash_ths
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_financial_cash_ths_provider import StockFinancialCashThsProvider


class StockFinancialCashThsService(BaseService):
    """现金流量表服务"""
    
    collection_name = "stock_financial_cash_ths"
    provider_class = StockFinancialCashThsProvider
    
    # 时间字段名
    time_field = "更新时间"
