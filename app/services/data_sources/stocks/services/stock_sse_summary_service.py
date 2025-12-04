"""
上海证券交易所服务

上海证券交易所-股票数据总貌
接口: stock_sse_summary
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_sse_summary_provider import StockSseSummaryProvider


class StockSseSummaryService(SimpleService):
    """上海证券交易所服务"""
    
    collection_name = "stock_sse_summary"
    provider_class = StockSseSummaryProvider
    
    # 时间字段名
    time_field = "更新时间"
