"""
业绩快报服务

东方财富-数据中心-年报季报-业绩快报
接口: stock_yjkb_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_yjkb_em_provider import StockYjkbEmProvider


class StockYjkbEmService(BaseService):
    """业绩快报服务"""
    
    collection_name = "stock_yjkb_em"
    provider_class = StockYjkbEmProvider
    
    # 时间字段名
    time_field = "更新时间"
