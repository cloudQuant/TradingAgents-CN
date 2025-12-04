"""
流通股东服务

新浪财经-股东股本-流通股东
接口: stock_circulate_stock_holder
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_circulate_stock_holder_provider import StockCirculateStockHolderProvider


class StockCirculateStockHolderService(BaseService):
    """流通股东服务"""
    
    collection_name = "stock_circulate_stock_holder"
    provider_class = StockCirculateStockHolderProvider
    
    # 时间字段名
    time_field = "更新时间"
