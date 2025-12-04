"""
基金持股服务

新浪财经-股本股东-基金持股
接口: stock_fund_stock_holder
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_fund_stock_holder_provider import StockFundStockHolderProvider


class StockFundStockHolderService(BaseService):
    """基金持股服务"""
    
    collection_name = "stock_fund_stock_holder"
    provider_class = StockFundStockHolderProvider
    
    # 时间字段名
    time_field = "更新时间"
