"""
分红派息服务

东方财富-港股-核心必读-分红派息
接口: stock_hk_dividend_payout_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hk_dividend_payout_em_provider import StockHkDividendPayoutEmProvider


class StockHkDividendPayoutEmService(BaseService):
    """分红派息服务"""
    
    collection_name = "stock_hk_dividend_payout_em"
    provider_class = StockHkDividendPayoutEmProvider
    
    # 时间字段名
    time_field = "更新时间"
