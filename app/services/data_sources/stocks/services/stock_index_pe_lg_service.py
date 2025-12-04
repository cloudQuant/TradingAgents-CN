"""
指数市盈率服务

乐咕乐股-指数市盈率
接口: stock_index_pe_lg
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_index_pe_lg_provider import StockIndexPeLgProvider


class StockIndexPeLgService(BaseService):
    """指数市盈率服务"""
    
    collection_name = "stock_index_pe_lg"
    provider_class = StockIndexPeLgProvider
    
    # 时间字段名
    time_field = "更新时间"
