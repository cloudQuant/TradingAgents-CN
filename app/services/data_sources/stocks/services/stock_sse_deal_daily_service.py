"""
上海证券交易所-每日概况服务

上海证券交易所-数据-股票数据-成交概况-股票成交概况-每日股票情况
接口: stock_sse_deal_daily
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_sse_deal_daily_provider import StockSseDealDailyProvider


class StockSseDealDailyService(BaseService):
    """上海证券交易所-每日概况服务"""
    
    collection_name = "stock_sse_deal_daily"
    provider_class = StockSseDealDailyProvider
    
    # 时间字段名
    time_field = "更新时间"
