"""
热搜股票服务

百度股市通-热搜股票
接口: stock_hot_search_baidu
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hot_search_baidu_provider import StockHotSearchBaiduProvider


class StockHotSearchBaiduService(BaseService):
    """热搜股票服务"""
    
    collection_name = "stock_hot_search_baidu"
    provider_class = StockHotSearchBaiduProvider
    
    # 时间字段名
    time_field = "更新时间"
