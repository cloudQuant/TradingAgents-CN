"""
昨日涨停股池服务

东方财富网-行情中心-涨停板行情-昨日涨停股池
接口: stock_zt_pool_previous_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zt_pool_previous_em_provider import StockZtPoolPreviousEmProvider


class StockZtPoolPreviousEmService(BaseService):
    """昨日涨停股池服务"""
    
    collection_name = "stock_zt_pool_previous_em"
    provider_class = StockZtPoolPreviousEmProvider
    
    # 时间字段名
    time_field = "更新时间"
