"""
新股服务

东方财富网-行情中心-沪深个股-新股
接口: stock_zh_a_new_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_zh_a_new_em_provider import StockZhANewEmProvider


class StockZhANewEmService(SimpleService):
    """新股服务"""
    
    collection_name = "stock_zh_a_new_em"
    provider_class = StockZhANewEmProvider
    
    # 时间字段名
    time_field = "更新时间"
