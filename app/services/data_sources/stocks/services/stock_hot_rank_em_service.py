"""
人气榜-A股服务

东方财富网站-股票热度
接口: stock_hot_rank_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_hot_rank_em_provider import StockHotRankEmProvider


class StockHotRankEmService(SimpleService):
    """人气榜-A股服务"""
    
    collection_name = "stock_hot_rank_em"
    provider_class = StockHotRankEmProvider
    
    # 时间字段名
    time_field = "更新时间"
