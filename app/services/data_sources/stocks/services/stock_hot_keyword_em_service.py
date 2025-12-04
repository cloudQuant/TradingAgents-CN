"""
热门关键词服务

东方财富-个股人气榜-热门关键词
接口: stock_hot_keyword_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hot_keyword_em_provider import StockHotKeywordEmProvider


class StockHotKeywordEmService(BaseService):
    """热门关键词服务"""
    
    collection_name = "stock_hot_keyword_em"
    provider_class = StockHotKeywordEmProvider
    
    # 时间字段名
    time_field = "更新时间"
