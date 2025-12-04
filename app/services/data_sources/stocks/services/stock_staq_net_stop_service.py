"""
两网及退市服务

东方财富网-行情中心-沪深个股-两网及退市
接口: stock_staq_net_stop
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_staq_net_stop_provider import StockStaqNetStopProvider


class StockStaqNetStopService(SimpleService):
    """两网及退市服务"""
    
    collection_name = "stock_staq_net_stop"
    provider_class = StockStaqNetStopProvider
    
    # 时间字段名
    time_field = "更新时间"
