"""
次新股池服务

东方财富网-行情中心-涨停板行情-次新股池
接口: stock_zt_pool_sub_new_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zt_pool_sub_new_em_provider import StockZtPoolSubNewEmProvider


class StockZtPoolSubNewEmService(BaseService):
    """次新股池服务"""
    
    collection_name = "stock_zt_pool_sub_new_em"
    provider_class = StockZtPoolSubNewEmProvider
    
    # 时间字段名
    time_field = "更新时间"
