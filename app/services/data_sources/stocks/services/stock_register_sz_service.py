"""
深圳主板服务

东方财富网-数据中心-新股数据-IPO审核信息-深圳主板
接口: stock_register_sz
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_register_sz_provider import StockRegisterSzProvider


class StockRegisterSzService(SimpleService):
    """深圳主板服务"""
    
    collection_name = "stock_register_sz"
    provider_class = StockRegisterSzProvider
    
    # 时间字段名
    time_field = "更新时间"
