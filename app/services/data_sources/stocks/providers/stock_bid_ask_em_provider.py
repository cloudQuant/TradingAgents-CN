"""
行情报价数据提供者

东方财富-行情报价
接口: stock_bid_ask_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockBidAskEmProvider(BaseProvider):
    """行情报价数据提供者"""
    
    # 必填属性
    collection_name = "stock_bid_ask_em"
    display_name = "行情报价"
    akshare_func = "stock_bid_ask_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-行情报价"
    collection_route = "/stocks/collections/stock_bid_ask_em"
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
        {"name": "item", "type": "object", "description": "-"},
        {"name": "value", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
