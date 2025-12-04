"""
风险警示板服务

东方财富网-行情中心-沪深个股-风险警示板
接口: stock_zh_a_st_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_zh_a_st_em_provider import StockZhAStEmProvider


class StockZhAStEmService(SimpleService):
    """风险警示板服务"""
    
    collection_name = "stock_zh_a_st_em"
    provider_class = StockZhAStEmProvider
    
    # 时间字段名
    time_field = "更新时间"
