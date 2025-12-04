"""
个股估值服务

东方财富网-数据中心-估值分析-每日互动-每日互动-估值分析
接口: stock_value_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_value_em_provider import StockValueEmProvider


class StockValueEmService(BaseService):
    """个股估值服务"""
    
    collection_name = "stock_value_em"
    provider_class = StockValueEmProvider
    
    # 时间字段名
    time_field = "更新时间"
