"""
股票更名服务

新浪财经-股票曾用名
接口: stock_info_change_name
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_info_change_name_provider import StockInfoChangeNameProvider


class StockInfoChangeNameService(BaseService):
    """股票更名服务"""
    
    collection_name = "stock_info_change_name"
    provider_class = StockInfoChangeNameProvider
    
    # 时间字段名
    time_field = "更新时间"
