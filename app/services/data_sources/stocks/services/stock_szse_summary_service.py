"""
证券类别统计服务

深圳证券交易所-市场总貌-证券类别统计
接口: stock_szse_summary
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_szse_summary_provider import StockSzseSummaryProvider


class StockSzseSummaryService(BaseService):
    """证券类别统计服务"""
    
    collection_name = "stock_szse_summary"
    provider_class = StockSzseSummaryProvider
    
    # 时间字段名
    time_field = "更新时间"
