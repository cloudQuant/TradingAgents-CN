"""
每日统计服务

东方财富网-数据中心-大宗交易-每日统计
接口: stock_dzjy_mrtj
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_dzjy_mrtj_provider import StockDzjyMrtjProvider


class StockDzjyMrtjService(BaseService):
    """每日统计服务"""
    
    collection_name = "stock_dzjy_mrtj"
    provider_class = StockDzjyMrtjProvider
    
    # 时间字段名
    time_field = "更新时间"
