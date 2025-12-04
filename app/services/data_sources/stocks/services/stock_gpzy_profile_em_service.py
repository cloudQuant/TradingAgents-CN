"""
股权质押市场概况服务

东方财富网-数据中心-特色数据-股权质押-股权质押市场概况
接口: stock_gpzy_profile_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_gpzy_profile_em_provider import StockGpzyProfileEmProvider


class StockGpzyProfileEmService(SimpleService):
    """股权质押市场概况服务"""
    
    collection_name = "stock_gpzy_profile_em"
    provider_class = StockGpzyProfileEmProvider
    
    # 时间字段名
    time_field = "更新时间"
