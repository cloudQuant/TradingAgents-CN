"""
创业板服务

东方财富网-数据中心-新股数据-IPO审核信息-创业板
接口: stock_register_cyb
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_register_cyb_provider import StockRegisterCybProvider


class StockRegisterCybService(SimpleService):
    """创业板服务"""
    
    collection_name = "stock_register_cyb"
    provider_class = StockRegisterCybProvider
    
    # 时间字段名
    time_field = "更新时间"
