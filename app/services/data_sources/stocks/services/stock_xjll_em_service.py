"""
现金流量表服务

东方财富-数据中心-年报季报-业绩快报-现金流量表
接口: stock_xjll_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_xjll_em_provider import StockXjllEmProvider


class StockXjllEmService(BaseService):
    """现金流量表服务"""
    
    collection_name = "stock_xjll_em"
    provider_class = StockXjllEmProvider
    
    # 时间字段名
    time_field = "更新时间"
