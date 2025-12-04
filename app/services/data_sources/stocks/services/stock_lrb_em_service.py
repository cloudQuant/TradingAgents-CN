"""
利润表服务

东方财富-数据中心-年报季报-业绩快报-利润表
接口: stock_lrb_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_lrb_em_provider import StockLrbEmProvider


class StockLrbEmService(BaseService):
    """利润表服务"""
    
    collection_name = "stock_lrb_em"
    provider_class = StockLrbEmProvider
    
    # 时间字段名
    time_field = "更新时间"
