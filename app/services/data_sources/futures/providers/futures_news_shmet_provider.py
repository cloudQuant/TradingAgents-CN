"""期货资讯提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesNewsShmetProvider(BaseProvider):
    """期货资讯提供者"""
    
    collection_name = "futures_news_shmet"
    display_name = "期货资讯"
    akshare_func = "futures_news_shmet"
    unique_keys = ["标题", "发布时间"]
    
    collection_description = "上海金属网期货资讯"
    collection_route = "/futures/collections/futures_news_shmet"
    collection_order = 52
    
    param_mapping = {"symbol": "symbol"}
    required_params = []
    
    field_info = [
        {"name": "标题", "type": "string", "description": "新闻标题"},
        {"name": "发布时间", "type": "string", "description": "发布时间"},
        {"name": "内容", "type": "string", "description": "新闻内容"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
