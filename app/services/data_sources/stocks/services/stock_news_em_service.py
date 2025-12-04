"""
个股新闻服务

东方财富指定个股的新闻资讯数据
接口: stock_news_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_news_em_provider import StockNewsEmProvider


class StockNewsEmService(BaseService):
    """个股新闻服务"""
    
    collection_name = "stock_news_em"
    provider_class = StockNewsEmProvider
    
    # 时间字段名
    time_field = "更新时间"
