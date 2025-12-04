"""
历史行情数据-新浪服务

美股历史行情数据，设定 adjust="qfq" 则返回前复权后的数据，默认 adjust="", 则返回未复权的数据，历史数据按日频率更新
接口: stock_us_daily
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_us_daily_provider import StockUsDailyProvider


class StockUsDailyService(BaseService):
    """历史行情数据-新浪服务"""
    
    collection_name = "stock_us_daily"
    provider_class = StockUsDailyProvider
    
    # 时间字段名
    time_field = "更新时间"
