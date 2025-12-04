"""
分时数据服务

新浪财经 B 股股票或者指数的分时数据，目前可以获取 1, 5, 15, 30, 60 分钟的数据频率, 可以指定是否复权
接口: stock_zh_b_minute
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zh_b_minute_provider import StockZhBMinuteProvider


class StockZhBMinuteService(BaseService):
    """分时数据服务"""
    
    collection_name = "stock_zh_b_minute"
    provider_class = StockZhBMinuteProvider
    
    # 时间字段名
    time_field = "更新时间"
