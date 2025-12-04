"""
个股估值数据提供者

东方财富网-数据中心-估值分析-每日互动-每日互动-估值分析
接口: stock_value_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockValueEmProvider(BaseProvider):
    """个股估值数据提供者"""
    
    # 必填属性
    collection_name = "stock_value_em"
    display_name = "个股估值"
    akshare_func = "stock_value_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-估值分析-每日互动-每日互动-估值分析"
    collection_route = "/stocks/collections/stock_value_em"
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
        {"name": "数据日期", "type": "object", "description": "-"},
        {"name": "当日收盘价", "type": "float64", "description": "注意单位: 元"},
        {"name": "当日涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "总市值", "type": "float64", "description": "注意单位: 元"},
        {"name": "流通市值", "type": "float64", "description": "注意单位: 元"},
        {"name": "总股本", "type": "float64", "description": "注意单位: 股"},
        {"name": "流通股本", "type": "float64", "description": "-"},
        {"name": "PE(TTM)", "type": "float64", "description": "-"},
        {"name": "PE(静)", "type": "float64", "description": "-"},
        {"name": "市净率", "type": "float64", "description": "-"},
        {"name": "PEG值", "type": "float64", "description": "-"},
        {"name": "市现率", "type": "float64", "description": "-"},
        {"name": "市销率", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
