"""
业绩预告服务

东方财富-数据中心-年报季报-业绩预告
接口: stock_yjyg_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_yjyg_em_provider import StockYjygEmProvider


class StockYjygEmService(BaseService):
    """业绩预告服务"""
    
    collection_name = "stock_yjyg_em"
    provider_class = StockYjygEmProvider
    
    # 时间字段名
    time_field = "更新时间"
