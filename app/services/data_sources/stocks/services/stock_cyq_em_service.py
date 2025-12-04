"""
筹码分布服务

东方财富网-概念板-行情中心-日K-筹码分布
接口: stock_cyq_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_cyq_em_provider import StockCyqEmProvider


class StockCyqEmService(BaseService):
    """筹码分布服务"""
    
    collection_name = "stock_cyq_em"
    provider_class = StockCyqEmProvider
    
    # 时间字段名
    time_field = "更新时间"
