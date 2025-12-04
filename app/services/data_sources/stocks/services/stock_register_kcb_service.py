"""
科创板服务

东方财富网-数据中心-新股数据-IPO审核信息-科创板
接口: stock_register_kcb
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_register_kcb_provider import StockRegisterKcbProvider


class StockRegisterKcbService(SimpleService):
    """科创板服务"""
    
    collection_name = "stock_register_kcb"
    provider_class = StockRegisterKcbProvider
    
    # 时间字段名
    time_field = "更新时间"
