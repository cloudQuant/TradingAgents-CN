"""
公司规模服务

东方财富-行情中心-同行比较-公司规模
接口: stock_zh_scale_comparison_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zh_scale_comparison_em_provider import StockZhScaleComparisonEmProvider


class StockZhScaleComparisonEmService(BaseService):
    """公司规模服务"""
    
    collection_name = "stock_zh_scale_comparison_em"
    provider_class = StockZhScaleComparisonEmProvider
    
    # 时间字段名
    time_field = "更新时间"
