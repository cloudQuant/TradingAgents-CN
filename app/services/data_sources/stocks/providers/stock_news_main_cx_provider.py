"""
财经内容精选数据提供者

财新网-财新数据通-内容精选
接口: stock_news_main_cx
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockNewsMainCxProvider(SimpleProvider):
    """财经内容精选数据提供者"""
    
    # 必填属性
    collection_name = "stock_news_main_cx"
    display_name = "财经内容精选"
    akshare_func = "stock_news_main_cx"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "财新网-财新数据通-内容精选"
    collection_route = "/stocks/collections/stock_news_main_cx"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "tag", "type": "object", "description": "-"},
        {"name": "summary", "type": "object", "description": "-"},
        {"name": "interval_time", "type": "object", "description": "-"},
        {"name": "pub_time", "type": "object", "description": "-"},
        {"name": "url", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
