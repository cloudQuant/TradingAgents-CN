"""
历史行情数据服务

腾讯财经-A+H 股数据
接口: stock_zh_ah_daily
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zh_ah_daily_provider import StockZhAhDailyProvider


class StockZhAhDailyService(BaseService):
    """历史行情数据服务"""
    
    collection_name = "stock_zh_ah_daily"
    provider_class = StockZhAhDailyProvider
    
    # 时间字段名
    time_field = "更新时间"
