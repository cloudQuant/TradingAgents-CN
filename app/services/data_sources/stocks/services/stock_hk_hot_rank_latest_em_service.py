"""
港股服务

东方财富-个股人气榜-最新排名
接口: stock_hk_hot_rank_latest_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hk_hot_rank_latest_em_provider import StockHkHotRankLatestEmProvider


class StockHkHotRankLatestEmService(BaseService):
    """港股服务"""
    
    collection_name = "stock_hk_hot_rank_latest_em"
    provider_class = StockHkHotRankLatestEmProvider
    
    # 时间字段名
    time_field = "更新时间"
