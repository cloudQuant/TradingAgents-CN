"""
A股服务

东方财富网-个股人气榜-实时变动
接口: stock_hot_rank_detail_realtime_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hot_rank_detail_realtime_em_provider import StockHotRankDetailRealtimeEmProvider


class StockHotRankDetailRealtimeEmService(BaseService):
    """A股服务"""
    
    collection_name = "stock_hot_rank_detail_realtime_em"
    provider_class = StockHotRankDetailRealtimeEmProvider
    
    # 时间字段名
    time_field = "更新时间"
