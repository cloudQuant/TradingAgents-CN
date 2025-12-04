"""
A股服务

东方财富网-股票热度-历史趋势及粉丝特征
接口: stock_hot_rank_detail_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hot_rank_detail_em_provider import StockHotRankDetailEmProvider


class StockHotRankDetailEmService(BaseService):
    """A股服务"""
    
    collection_name = "stock_hot_rank_detail_em"
    provider_class = StockHotRankDetailEmProvider
    
    # 时间字段名
    time_field = "更新时间"
