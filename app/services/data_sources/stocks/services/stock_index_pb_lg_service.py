"""
指数市净率服务

乐咕乐股-指数市净率
接口: stock_index_pb_lg
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_index_pb_lg_provider import StockIndexPbLgProvider


class StockIndexPbLgService(BaseService):
    """指数市净率服务"""
    
    collection_name = "stock_index_pb_lg"
    provider_class = StockIndexPbLgProvider
    
    # 时间字段名
    time_field = "更新时间"
