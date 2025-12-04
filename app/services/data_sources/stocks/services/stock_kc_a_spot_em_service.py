"""
科创板服务

东方财富网-科创板-实时行情
接口: stock_kc_a_spot_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_kc_a_spot_em_provider import StockKcASpotEmProvider


class StockKcASpotEmService(SimpleService):
    """科创板服务"""
    
    collection_name = "stock_kc_a_spot_em"
    provider_class = StockKcASpotEmProvider
    
    # 时间字段名
    time_field = "更新时间"
