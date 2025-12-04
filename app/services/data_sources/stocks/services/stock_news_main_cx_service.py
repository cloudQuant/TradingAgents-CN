"""
财经内容精选服务

财新网-财新数据通-内容精选
接口: stock_news_main_cx
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_news_main_cx_provider import StockNewsMainCxProvider


class StockNewsMainCxService(SimpleService):
    """财经内容精选服务"""
    
    collection_name = "stock_news_main_cx"
    provider_class = StockNewsMainCxProvider
    
    # 时间字段名
    time_field = "更新时间"
