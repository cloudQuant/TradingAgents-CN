"""
创新高和新低的股票数量服务

不同市场的创新高和新低的股票数量
接口: stock_a_high_low_statistics
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_a_high_low_statistics_provider import StockAHighLowStatisticsProvider


class StockAHighLowStatisticsService(BaseService):
    """创新高和新低的股票数量服务"""
    
    collection_name = "stock_a_high_low_statistics"
    provider_class = StockAHighLowStatisticsProvider
    
    # 时间字段名
    time_field = "更新时间"
