"""
历史行情数据服务

B 股数据是从新浪财经获取的数据, 历史数据按日频率更新
接口: stock_zh_b_daily
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zh_b_daily_provider import StockZhBDailyProvider


class StockZhBDailyService(BaseService):
    """历史行情数据服务"""
    
    collection_name = "stock_zh_b_daily"
    provider_class = StockZhBDailyProvider
    
    # 时间字段名
    time_field = "更新时间"
