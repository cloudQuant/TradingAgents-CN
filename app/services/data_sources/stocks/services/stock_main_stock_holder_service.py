"""
主要股东服务

新浪财经-股本股东-主要股东
接口: stock_main_stock_holder
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_main_stock_holder_provider import StockMainStockHolderProvider


class StockMainStockHolderService(BaseService):
    """主要股东服务"""
    
    collection_name = "stock_main_stock_holder"
    provider_class = StockMainStockHolderProvider
    
    # 时间字段名
    time_field = "更新时间"
