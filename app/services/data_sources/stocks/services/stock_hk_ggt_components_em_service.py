"""
港股通成份股服务

东方财富网-行情中心-港股市场-港股通成份股
接口: stock_hk_ggt_components_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_hk_ggt_components_em_provider import StockHkGgtComponentsEmProvider


class StockHkGgtComponentsEmService(SimpleService):
    """港股通成份股服务"""
    
    collection_name = "stock_hk_ggt_components_em"
    provider_class = StockHkGgtComponentsEmProvider
    
    # 时间字段名
    time_field = "更新时间"
