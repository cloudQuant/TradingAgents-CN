"""
跌停股池服务

东方财富网-行情中心-涨停板行情-跌停股池
接口: stock_zt_pool_dtgc_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zt_pool_dtgc_em_provider import StockZtPoolDtgcEmProvider


class StockZtPoolDtgcEmService(BaseService):
    """跌停股池服务"""
    
    collection_name = "stock_zt_pool_dtgc_em"
    provider_class = StockZtPoolDtgcEmProvider
    
    # 时间字段名
    time_field = "更新时间"
