"""
持续放量服务

同花顺-数据中心-技术选股-持续放量
接口: stock_rank_cxfl_ths
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_rank_cxfl_ths_provider import StockRankCxflThsProvider


class StockRankCxflThsService(SimpleService):
    """持续放量服务"""
    
    collection_name = "stock_rank_cxfl_ths"
    provider_class = StockRankCxflThsProvider
    
    # 时间字段名
    time_field = "更新时间"
