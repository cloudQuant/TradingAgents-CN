"""
交易排行榜服务

雪球-沪深股市-热度排行榜-交易排行榜
接口: stock_hot_deal_xq
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hot_deal_xq_provider import StockHotDealXqProvider


class StockHotDealXqService(BaseService):
    """交易排行榜服务"""
    
    collection_name = "stock_hot_deal_xq"
    provider_class = StockHotDealXqProvider
    
    # 时间字段名
    time_field = "更新时间"
