"""
实时行情数据-新浪服务

获取所有港股的实时行情数据 15 分钟延时
接口: stock_hk_spot
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_hk_spot_provider import StockHkSpotProvider


class StockHkSpotService(SimpleService):
    """实时行情数据-新浪服务"""
    
    collection_name = "stock_hk_spot"
    provider_class = StockHkSpotProvider
    
    # 时间字段名
    time_field = "更新时间"
