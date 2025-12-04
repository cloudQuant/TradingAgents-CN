"""
成长性比较服务

东方财富-行情中心-同行比较-成长性比较
接口: stock_zh_growth_comparison_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zh_growth_comparison_em_provider import StockZhGrowthComparisonEmProvider


class StockZhGrowthComparisonEmService(BaseService):
    """成长性比较服务"""
    
    collection_name = "stock_zh_growth_comparison_em"
    provider_class = StockZhGrowthComparisonEmProvider
    
    # 时间字段名
    time_field = "更新时间"
