"""
险资举牌服务

同花顺-数据中心-技术选股-险资举牌
接口: stock_rank_xzjp_ths
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_rank_xzjp_ths_provider import StockRankXzjpThsProvider


class StockRankXzjpThsService(SimpleService):
    """险资举牌服务"""
    
    collection_name = "stock_rank_xzjp_ths"
    provider_class = StockRankXzjpThsProvider
    
    # 时间字段名
    time_field = "更新时间"
