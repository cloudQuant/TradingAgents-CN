"""
分时数据-新浪服务

新浪财经-沪深京 A 股股票或者指数的分时数据，目前可以获取 1, 5, 15, 30, 60 分钟的数据频率, 可以指定是否复权
接口: stock_zh_a_minute
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zh_a_minute_provider import StockZhAMinuteProvider


class StockZhAMinuteService(BaseService):
    """分时数据-新浪服务"""
    
    collection_name = "stock_zh_a_minute"
    provider_class = StockZhAMinuteProvider
    
    # 时间字段名
    time_field = "更新时间"
