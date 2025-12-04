"""
量价齐跌服务

同花顺-数据中心-技术选股-量价齐跌
接口: stock_rank_ljqd_ths
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_rank_ljqd_ths_provider import StockRankLjqdThsProvider


class StockRankLjqdThsService(SimpleService):
    """量价齐跌服务"""
    
    collection_name = "stock_rank_ljqd_ths"
    provider_class = StockRankLjqdThsProvider
    
    # 时间字段名
    time_field = "更新时间"
