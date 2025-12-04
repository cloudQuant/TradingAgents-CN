"""
热门关键词数据提供者

东方财富-个股人气榜-热门关键词
接口: stock_hot_keyword_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockHotKeywordEmProvider(BaseProvider):
    """热门关键词数据提供者"""
    
    # 必填属性
    collection_name = "stock_hot_keyword_em"
    display_name = "热门关键词"
    akshare_func = "stock_hot_keyword_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富-个股人气榜-热门关键词"
    collection_route = "/stocks/collections/stock_hot_keyword_em"
    collection_category = "热门排行"

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
        {"name": "时间", "type": "object", "description": "-"},
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "概念代码", "type": "object", "description": "-"},
        {"name": "热度", "type": "int64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
