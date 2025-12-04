"""
股东户数服务

东方财富网-数据中心-特色数据-股东户数数据
接口: stock_zh_a_gdhs
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zh_a_gdhs_provider import StockZhAGdhsProvider


class StockZhAGdhsService(BaseService):
    """股东户数服务"""
    
    collection_name = "stock_zh_a_gdhs"
    provider_class = StockZhAGdhsProvider
    
    # 时间字段名
    time_field = "更新时间"
