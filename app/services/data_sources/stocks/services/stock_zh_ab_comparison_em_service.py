"""
AB 股比价服务

东方财富网-行情中心-沪深京个股-AB股比价-全部AB股比价
接口: stock_zh_ab_comparison_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_zh_ab_comparison_em_provider import StockZhAbComparisonEmProvider


class StockZhAbComparisonEmService(SimpleService):
    """AB 股比价服务"""
    
    collection_name = "stock_zh_ab_comparison_em"
    provider_class = StockZhAbComparisonEmProvider
    
    # 时间字段名
    time_field = "更新时间"
