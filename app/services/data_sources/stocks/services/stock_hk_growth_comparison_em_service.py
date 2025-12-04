"""
成长性对比服务

东方财富-港股-行业对比-成长性对比
接口: stock_hk_growth_comparison_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hk_growth_comparison_em_provider import StockHkGrowthComparisonEmProvider


class StockHkGrowthComparisonEmService(BaseService):
    """成长性对比服务"""
    
    collection_name = "stock_hk_growth_comparison_em"
    provider_class = StockHkGrowthComparisonEmProvider
    
    # 时间字段名
    time_field = "更新时间"
