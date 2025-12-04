"""
创业板服务

东方财富网-创业板-实时行情
接口: stock_cy_a_spot_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_cy_a_spot_em_provider import StockCyASpotEmProvider


class StockCyASpotEmService(SimpleService):
    """创业板服务"""
    
    collection_name = "stock_cy_a_spot_em"
    provider_class = StockCyASpotEmProvider
    
    # 时间字段名
    time_field = "更新时间"
