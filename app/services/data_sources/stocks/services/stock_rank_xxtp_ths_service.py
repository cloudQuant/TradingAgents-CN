"""
向下突破服务

同花顺-数据中心-技术选股-向下突破
接口: stock_rank_xxtp_ths
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_rank_xxtp_ths_provider import StockRankXxtpThsProvider


class StockRankXxtpThsService(BaseService):
    """向下突破服务"""
    
    collection_name = "stock_rank_xxtp_ths"
    provider_class = StockRankXxtpThsProvider
    
    # 时间字段名
    time_field = "更新时间"
