"""
股票行业成交服务

深圳证券交易所-统计资料-股票行业成交数据
接口: stock_szse_sector_summary
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_szse_sector_summary_provider import StockSzseSectorSummaryProvider


class StockSzseSectorSummaryService(BaseService):
    """股票行业成交服务"""
    
    collection_name = "stock_szse_sector_summary"
    provider_class = StockSzseSectorSummaryProvider
    
    # 时间字段名
    time_field = "更新时间"
