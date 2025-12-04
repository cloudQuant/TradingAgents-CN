"""
历史分红服务

新浪财经-发行与分配-历史分红
接口: stock_history_dividend
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_history_dividend_provider import StockHistoryDividendProvider


class StockHistoryDividendService(SimpleService):
    """历史分红服务"""
    
    collection_name = "stock_history_dividend"
    provider_class = StockHistoryDividendProvider
    
    # 时间字段名
    time_field = "更新时间"
