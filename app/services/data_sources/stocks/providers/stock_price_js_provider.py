"""
美港目标价数据提供者

美港电讯-美港目标价数据
接口: stock_price_js
"""
from app.services.data_sources.base_provider import BaseProvider


class StockPriceJsProvider(BaseProvider):
    """美港目标价数据提供者"""
    
    # 必填属性
    collection_name = "stock_price_js"
    display_name = "美港目标价"
    akshare_func = "stock_price_js"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "美港电讯-美港目标价数据"
    collection_route = "/stocks/collections/stock_price_js"
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
        {"name": "日期", "type": "object", "description": "-"},
        {"name": "评级", "type": "object", "description": "-"},
        {"name": "先前目标价", "type": "float64", "description": "-"},
        {"name": "最新目标价", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
