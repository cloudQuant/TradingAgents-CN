"""
港股服务

东方财富网-股票热度-历史趋势
接口: stock_hk_hot_rank_detail_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hk_hot_rank_detail_em_provider import StockHkHotRankDetailEmProvider


class StockHkHotRankDetailEmService(BaseService):
    """港股服务"""
    
    collection_name = "stock_hk_hot_rank_detail_em"
    provider_class = StockHkHotRankDetailEmProvider
    
    # 时间字段名
    time_field = "更新时间"
