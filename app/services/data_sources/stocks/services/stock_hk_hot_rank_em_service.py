"""
人气榜-港股服务

东方财富-个股人气榜-人气榜-港股市场
接口: stock_hk_hot_rank_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_hk_hot_rank_em_provider import StockHkHotRankEmProvider


class StockHkHotRankEmService(SimpleService):
    """人气榜-港股服务"""
    
    collection_name = "stock_hk_hot_rank_em"
    provider_class = StockHkHotRankEmProvider
    
    # 时间字段名
    time_field = "更新时间"
