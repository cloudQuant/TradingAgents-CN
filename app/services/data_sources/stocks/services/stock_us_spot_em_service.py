"""
实时行情数据-东财服务

东方财富网-美股-实时行情
接口: stock_us_spot_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_us_spot_em_provider import StockUsSpotEmProvider


class StockUsSpotEmService(SimpleService):
    """实时行情数据-东财服务"""
    
    collection_name = "stock_us_spot_em"
    provider_class = StockUsSpotEmProvider
    
    # 时间字段名
    time_field = "更新时间"
