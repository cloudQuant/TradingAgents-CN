"""
日内分时数据-新浪数据提供者

新浪财经-日内分时数据
接口: stock_intraday_sina
"""
from app.services.data_sources.base_provider import BaseProvider


class StockIntradaySinaProvider(BaseProvider):
    """日内分时数据-新浪数据提供者"""
    
    # 必填属性
    collection_name = "stock_intraday_sina"
    display_name = "日内分时数据-新浪"
    akshare_func = "stock_intraday_sina"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪财经-日内分时数据"
    collection_route = "/stocks/collections/stock_intraday_sina"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "date": "date"
    }
    
    # 必填参数
    required_params = ['symbol', 'date']

    # 字段信息
    field_info = [
        {"name": "symbol", "type": "object", "description": "-"},
        {"name": "name", "type": "object", "description": "-"},
        {"name": "ticktime", "type": "object", "description": "-"},
        {"name": "price", "type": "float64", "description": "-"},
        {"name": "volume", "type": "int64", "description": "注意单位: 股"},
        {"name": "prev_price", "type": "float64", "description": "-"},
        {"name": "kind", "type": "object", "description": "D 表示卖盘，表示 是买盘"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
