"""
重大合同服务

东方财富网-数据中心-重大合同-重大合同明细
接口: stock_zdhtmx_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zdhtmx_em_provider import StockZdhtmxEmProvider


class StockZdhtmxEmService(BaseService):
    """重大合同服务"""
    
    collection_name = "stock_zdhtmx_em"
    provider_class = StockZdhtmxEmProvider
    
    # 时间字段名
    time_field = "更新时间"
