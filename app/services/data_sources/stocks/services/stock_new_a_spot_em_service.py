"""
新股服务

东方财富网-新股-实时行情数据
接口: stock_new_a_spot_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_new_a_spot_em_provider import StockNewASpotEmProvider


class StockNewASpotEmService(SimpleService):
    """新股服务"""
    
    collection_name = "stock_new_a_spot_em"
    provider_class = StockNewASpotEmProvider
    
    # 时间字段名
    time_field = "更新时间"
