"""
飙升榜-A股服务

东方财富-个股人气榜-飙升榜
接口: stock_hot_up_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_hot_up_em_provider import StockHotUpEmProvider


class StockHotUpEmService(SimpleService):
    """飙升榜-A股服务"""
    
    collection_name = "stock_hot_up_em"
    provider_class = StockHotUpEmProvider
    
    # 时间字段名
    time_field = "更新时间"
