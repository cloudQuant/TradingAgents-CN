"""
行情报价服务

东方财富-行情报价
接口: stock_bid_ask_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_bid_ask_em_provider import StockBidAskEmProvider


class StockBidAskEmService(BaseService):
    """行情报价服务"""
    
    collection_name = "stock_bid_ask_em"
    provider_class = StockBidAskEmProvider
    
    # 时间字段名
    time_field = "更新时间"
