"""
两网及退市服务

东方财富网-行情中心-沪深个股-两网及退市
接口: stock_zh_a_stop_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_zh_a_stop_em_provider import StockZhAStopEmProvider


class StockZhAStopEmService(SimpleService):
    """两网及退市服务"""
    
    collection_name = "stock_zh_a_stop_em"
    provider_class = StockZhAStopEmProvider
    
    # 时间字段名
    time_field = "更新时间"
