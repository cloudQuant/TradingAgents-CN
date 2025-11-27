"""
股票型基金仓位-理杏仁服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_stock_position_lg_provider import FundStockPositionLgProvider


class FundStockPositionLgService(SimpleService):
    """股票型基金仓位-理杏仁服务"""
    
    collection_name = "fund_stock_position_lg"
    provider_class = FundStockPositionLgProvider
