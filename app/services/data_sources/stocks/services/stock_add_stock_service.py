"""
股票增发服务

新浪财经-发行与分配-增发
接口: stock_add_stock
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_add_stock_provider import StockAddStockProvider


class StockAddStockService(BaseService):
    """股票增发服务"""
    
    collection_name = "stock_add_stock"
    provider_class = StockAddStockProvider
    
    # 时间字段名
    time_field = "更新时间"
