"""
粉单市场服务

美股粉单市场的实时行情数据
接口: stock_us_pink_spot_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_us_pink_spot_em_provider import StockUsPinkSpotEmProvider


class StockUsPinkSpotEmService(SimpleService):
    """粉单市场服务"""
    
    collection_name = "stock_us_pink_spot_em"
    provider_class = StockUsPinkSpotEmProvider
    
    # 时间字段名
    time_field = "更新时间"
