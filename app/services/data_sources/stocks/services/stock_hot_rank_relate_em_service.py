"""
相关股票服务

东方财富-个股人气榜-相关股票
接口: stock_hot_rank_relate_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hot_rank_relate_em_provider import StockHotRankRelateEmProvider


class StockHotRankRelateEmService(BaseService):
    """相关股票服务"""
    
    collection_name = "stock_hot_rank_relate_em"
    provider_class = StockHotRankRelateEmProvider
    
    # 时间字段名
    time_field = "更新时间"
