"""
股票更名数据提供者

新浪财经-股票曾用名
接口: stock_info_change_name
"""
from app.services.data_sources.base_provider import BaseProvider


class StockInfoChangeNameProvider(BaseProvider):
    """股票更名数据提供者"""
    
    # 必填属性
    collection_name = "stock_info_change_name"
    display_name = "股票更名"
    akshare_func = "stock_info_change_name"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪财经-股票曾用名"
    collection_route = "/stocks/collections/stock_info_change_name"
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
        {"name": "index", "type": "int64", "description": "-"},
        {"name": "name", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
