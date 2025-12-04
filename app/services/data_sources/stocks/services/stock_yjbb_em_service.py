"""
业绩报表服务

东方财富-数据中心-年报季报-业绩报表
接口: stock_yjbb_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_yjbb_em_provider import StockYjbbEmProvider


class StockYjbbEmService(BaseService):
    """业绩报表服务"""
    
    collection_name = "stock_yjbb_em"
    provider_class = StockYjbbEmProvider
    
    # 时间字段名
    time_field = "更新时间"
