"""
个股新闻数据提供者

东方财富指定个股的新闻资讯数据
接口: stock_news_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockNewsEmProvider(BaseProvider):
    """个股新闻数据提供者"""
    
    # 必填属性
    collection_name = "stock_news_em"
    display_name = "个股新闻"
    akshare_func = "stock_news_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富指定个股的新闻资讯数据"
    collection_route = "/stocks/collections/stock_news_em"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol"
    }
    
    # 必填参数
    required_params = ['symbol']

    # 字段信息
    field_info = [
        {"name": "关键词", "type": "object", "description": "-"},
        {"name": "新闻标题", "type": "object", "description": "-"},
        {"name": "新闻内容", "type": "object", "description": "-"},
        {"name": "发布时间", "type": "object", "description": "-"},
        {"name": "文章来源", "type": "object", "description": "-"},
        {"name": "新闻链接", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
