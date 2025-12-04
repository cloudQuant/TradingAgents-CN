"""
股东大会服务

东方财富网-数据中心-股东大会
接口: stock_gddh_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_gddh_em_provider import StockGddhEmProvider


class StockGddhEmService(SimpleService):
    """股东大会服务"""
    
    collection_name = "stock_gddh_em"
    provider_class = StockGddhEmProvider
    
    # 时间字段名
    time_field = "更新时间"
