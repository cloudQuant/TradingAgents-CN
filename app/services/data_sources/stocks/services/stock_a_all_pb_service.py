"""
A 股等权重与中位数市净率服务

乐咕乐股-A 股等权重与中位数市净率
接口: stock_a_all_pb
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_a_all_pb_provider import StockAAllPbProvider


class StockAAllPbService(SimpleService):
    """A 股等权重与中位数市净率服务"""
    
    collection_name = "stock_a_all_pb"
    provider_class = StockAAllPbProvider
    
    # 时间字段名
    time_field = "更新时间"
