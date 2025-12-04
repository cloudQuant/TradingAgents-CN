"""
讨论排行榜服务

雪球-沪深股市-热度排行榜-讨论排行榜
接口: stock_hot_tweet_xq
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hot_tweet_xq_provider import StockHotTweetXqProvider


class StockHotTweetXqService(BaseService):
    """讨论排行榜服务"""
    
    collection_name = "stock_hot_tweet_xq"
    provider_class = StockHotTweetXqProvider
    
    # 时间字段名
    time_field = "更新时间"
