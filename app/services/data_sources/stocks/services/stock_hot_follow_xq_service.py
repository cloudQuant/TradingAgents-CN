"""
关注排行榜服务

雪球-沪深股市-热度排行榜-关注排行榜
接口: stock_hot_follow_xq
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hot_follow_xq_provider import StockHotFollowXqProvider


class StockHotFollowXqService(BaseService):
    """关注排行榜服务"""
    
    collection_name = "stock_hot_follow_xq"
    provider_class = StockHotFollowXqProvider
    
    # 时间字段名
    time_field = "更新时间"
