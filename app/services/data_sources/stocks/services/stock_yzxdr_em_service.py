"""
一致行动人服务

东方财富网-数据中心-特色数据-一致行动人
接口: stock_yzxdr_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_yzxdr_em_provider import StockYzxdrEmProvider


class StockYzxdrEmService(BaseService):
    """一致行动人服务"""
    
    collection_name = "stock_yzxdr_em"
    provider_class = StockYzxdrEmProvider
    
    # 时间字段名
    time_field = "更新时间"
