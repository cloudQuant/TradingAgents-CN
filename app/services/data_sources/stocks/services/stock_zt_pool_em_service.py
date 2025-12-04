"""
涨停股池服务

东方财富网-行情中心-涨停板行情-涨停股池
接口: stock_zt_pool_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zt_pool_em_provider import StockZtPoolEmProvider


class StockZtPoolEmService(BaseService):
    """涨停股池服务"""
    
    collection_name = "stock_zt_pool_em"
    provider_class = StockZtPoolEmProvider
    
    # 时间字段名
    time_field = "更新时间"
