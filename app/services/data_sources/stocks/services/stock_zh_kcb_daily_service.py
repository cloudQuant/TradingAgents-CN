"""
历史行情数据服务

新浪财经-科创板股票历史行情数据
接口: stock_zh_kcb_daily
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zh_kcb_daily_provider import StockZhKcbDailyProvider


class StockZhKcbDailyService(BaseService):
    """历史行情数据服务"""
    
    collection_name = "stock_zh_kcb_daily"
    provider_class = StockZhKcbDailyProvider
    
    # 时间字段名
    time_field = "更新时间"
