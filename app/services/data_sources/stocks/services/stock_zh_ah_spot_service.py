"""
实时行情数据-腾讯服务

A+H 股数据是从腾讯财经获取的数据, 延迟 15 分钟更新
接口: stock_zh_ah_spot
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_zh_ah_spot_provider import StockZhAhSpotProvider


class StockZhAhSpotService(SimpleService):
    """实时行情数据-腾讯服务"""
    
    collection_name = "stock_zh_ah_spot"
    provider_class = StockZhAhSpotProvider
    
    # 时间字段名
    time_field = "更新时间"
