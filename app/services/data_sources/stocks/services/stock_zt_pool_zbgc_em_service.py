"""
炸板股池服务

东方财富网-行情中心-涨停板行情-炸板股池
接口: stock_zt_pool_zbgc_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zt_pool_zbgc_em_provider import StockZtPoolZbgcEmProvider


class StockZtPoolZbgcEmService(BaseService):
    """炸板股池服务"""
    
    collection_name = "stock_zt_pool_zbgc_em"
    provider_class = StockZtPoolZbgcEmProvider
    
    # 时间字段名
    time_field = "更新时间"
