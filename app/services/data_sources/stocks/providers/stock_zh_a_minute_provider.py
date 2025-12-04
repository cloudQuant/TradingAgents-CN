"""
分时数据-新浪数据提供者

新浪财经-沪深京 A 股股票或者指数的分时数据，目前可以获取 1, 5, 15, 30, 60 分钟的数据频率, 可以指定是否复权
接口: stock_zh_a_minute
"""
from app.services.data_sources.base_provider import BaseProvider


class StockZhAMinuteProvider(BaseProvider):
    """分时数据-新浪数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_a_minute"
    display_name = "分时数据-新浪"
    akshare_func = "stock_zh_a_minute"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "新浪财经-沪深京 A 股股票或者指数的分时数据，目前可以获取 1, 5, 15, 30, 60 分钟的数据频率, 可以指定是否复权"
    collection_route = "/stocks/collections/stock_zh_a_minute"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "period": "period",
        "adjust": "adjust"
    }
    
    # 必填参数
    required_params = ['symbol', 'period']

    # 字段信息
    field_info = [
        {"name": "day", "type": "object", "description": "-"},
        {"name": "open", "type": "float64", "description": "-"},
        {"name": "high", "type": "float64", "description": "-"},
        {"name": "low", "type": "float64", "description": "-"},
        {"name": "close", "type": "float64", "description": "-"},
        {"name": "volume", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
