"""
规模对比服务

东方财富-港股-行业对比-规模对比
接口: stock_hk_scale_comparison_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hk_scale_comparison_em_provider import StockHkScaleComparisonEmProvider


class StockHkScaleComparisonEmService(BaseService):
    """规模对比服务"""
    
    collection_name = "stock_hk_scale_comparison_em"
    provider_class = StockHkScaleComparisonEmProvider
    
    # 时间字段名
    time_field = "更新时间"
