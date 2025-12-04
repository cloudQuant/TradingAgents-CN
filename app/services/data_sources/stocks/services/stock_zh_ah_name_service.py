"""
A+H股票字典服务

A+H 股数据是从腾讯财经获取的数据, 历史数据按日频率更新
接口: stock_zh_ah_name
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_zh_ah_name_provider import StockZhAhNameProvider


class StockZhAhNameService(SimpleService):
    """A+H股票字典服务"""
    
    collection_name = "stock_zh_ah_name"
    provider_class = StockZhAhNameProvider
    
    # 时间字段名
    time_field = "更新时间"
