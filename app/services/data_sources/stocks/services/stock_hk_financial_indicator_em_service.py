"""
财务指标服务

东方财富-港股-核心必读-最新指标
接口: stock_hk_financial_indicator_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hk_financial_indicator_em_provider import StockHkFinancialIndicatorEmProvider


class StockHkFinancialIndicatorEmService(BaseService):
    """财务指标服务"""
    
    collection_name = "stock_hk_financial_indicator_em"
    provider_class = StockHkFinancialIndicatorEmProvider
    
    # 时间字段名
    time_field = "更新时间"
