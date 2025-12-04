"""
每日个股统计服务

东方财富网-数据中心-沪深港通-沪深港通持股-每日个股统计
接口: stock_hsgt_stock_statistics_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hsgt_stock_statistics_em_provider import StockHsgtStockStatisticsEmProvider


class StockHsgtStockStatisticsEmService(BaseService):
    """每日个股统计服务"""
    
    collection_name = "stock_hsgt_stock_statistics_em"
    provider_class = StockHsgtStockStatisticsEmProvider
    
    # 时间字段名
    time_field = "更新时间"
