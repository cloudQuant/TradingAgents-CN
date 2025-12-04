"""
股本结构服务

东方财富-A股数据-股本结构
接口: stock_zh_a_gbjg_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zh_a_gbjg_em_provider import StockZhAGbjgEmProvider


class StockZhAGbjgEmService(BaseService):
    """股本结构服务"""
    
    collection_name = "stock_zh_a_gbjg_em"
    provider_class = StockZhAGbjgEmProvider
    
    # 时间字段名
    time_field = "更新时间"
