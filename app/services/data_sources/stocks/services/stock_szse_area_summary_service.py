"""
地区交易排序服务

深圳证券交易所-市场总貌-地区交易排序
接口: stock_szse_area_summary
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_szse_area_summary_provider import StockSzseAreaSummaryProvider


class StockSzseAreaSummaryService(BaseService):
    """地区交易排序服务"""
    
    collection_name = "stock_szse_area_summary"
    provider_class = StockSzseAreaSummaryProvider
    
    # 时间字段名
    time_field = "更新时间"
