"""
分红配股服务

新浪财经-发行与分配-分红配股
接口: stock_history_dividend_detail
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_history_dividend_detail_provider import StockHistoryDividendDetailProvider


class StockHistoryDividendDetailService(BaseService):
    """分红配股服务"""
    
    collection_name = "stock_history_dividend_detail"
    provider_class = StockHistoryDividendDetailProvider
    
    # 时间字段名
    time_field = "更新时间"
