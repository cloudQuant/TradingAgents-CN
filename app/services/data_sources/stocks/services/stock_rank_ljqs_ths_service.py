"""
量价齐升服务

同花顺-数据中心-技术选股-量价齐升
接口: stock_rank_ljqs_ths
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_rank_ljqs_ths_provider import StockRankLjqsThsProvider


class StockRankLjqsThsService(SimpleService):
    """量价齐升服务"""
    
    collection_name = "stock_rank_ljqs_ths"
    provider_class = StockRankLjqsThsProvider
    
    # 时间字段名
    time_field = "更新时间"
