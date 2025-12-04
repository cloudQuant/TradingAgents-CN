"""
配股服务

东方财富网-数据中心-新股数据-配股
接口: stock_pg_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_pg_em_provider import StockPgEmProvider


class StockPgEmService(SimpleService):
    """配股服务"""
    
    collection_name = "stock_pg_em"
    provider_class = StockPgEmProvider
    
    # 时间字段名
    time_field = "更新时间"
