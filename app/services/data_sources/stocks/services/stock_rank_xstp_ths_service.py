"""
向上突破服务

同花顺-数据中心-技术选股-向上突破
接口: stock_rank_xstp_ths
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_rank_xstp_ths_provider import StockRankXstpThsProvider


class StockRankXstpThsService(BaseService):
    """向上突破服务"""
    
    collection_name = "stock_rank_xstp_ths"
    provider_class = StockRankXstpThsProvider
    
    # 时间字段名
    time_field = "更新时间"
