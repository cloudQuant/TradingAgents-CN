"""
主板市盈率服务

乐咕乐股-主板市盈率
接口: stock_market_pe_lg
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_market_pe_lg_provider import StockMarketPeLgProvider


class StockMarketPeLgService(BaseService):
    """主板市盈率服务"""
    
    collection_name = "stock_market_pe_lg"
    provider_class = StockMarketPeLgProvider
    
    # 时间字段名
    time_field = "更新时间"
