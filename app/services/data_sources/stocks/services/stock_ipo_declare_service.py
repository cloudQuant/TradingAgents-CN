"""
首发申报信息服务

东方财富网-数据中心-新股申购-首发申报信息-首发申报企业信息
接口: stock_ipo_declare
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_ipo_declare_provider import StockIpoDeclareProvider


class StockIpoDeclareService(SimpleService):
    """首发申报信息服务"""
    
    collection_name = "stock_ipo_declare"
    provider_class = StockIpoDeclareProvider
    
    # 时间字段名
    time_field = "更新时间"
