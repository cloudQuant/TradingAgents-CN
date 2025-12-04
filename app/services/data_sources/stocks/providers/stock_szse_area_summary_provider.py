"""
地区交易排序数据提供者

深圳证券交易所-市场总貌-地区交易排序
接口: stock_szse_area_summary
"""
from app.services.data_sources.base_provider import BaseProvider


class StockSzseAreaSummaryProvider(BaseProvider):
    """地区交易排序数据提供者"""
    
    # 必填属性
    collection_name = "stock_szse_area_summary"
    display_name = "地区交易排序"
    akshare_func = "stock_szse_area_summary"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "深圳证券交易所-市场总貌-地区交易排序"
    collection_route = "/stocks/collections/stock_szse_area_summary"
    collection_category = "默认"

    # 参数映射
    param_mapping = {
        "date": "date"
    }
    
    # 必填参数
    required_params = ['date']

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "地区", "type": "object", "description": "-"},
        {"name": "总交易额", "type": "float64", "description": "注意单位: 元"},
        {"name": "占市场", "type": "float64", "description": "注意单位: %"},
        {"name": "股票交易额", "type": "float64", "description": "注意单位: 元"},
        {"name": "基金交易额", "type": "float64", "description": "注意单位: 元"},
        {"name": "债券交易额", "type": "float64", "description": "注意单位: 元"},
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "地区", "type": "object", "description": "-"},
        {"name": "总交易额", "type": "float64", "description": "注意单位: 元"},
        {"name": "占市场", "type": "float64", "description": "注意单位: %"},
        {"name": "股票交易额", "type": "float64", "description": "注意单位: 元"},
        {"name": "基金交易额", "type": "float64", "description": "注意单位: 元"},
        {"name": "债券交易额", "type": "float64", "description": "注意单位: 元"},
        {"name": "优先股交易额", "type": "float64", "description": "注意单位: 元"},
        {"name": "期权交易额", "type": "float64", "description": "注意单位: 元"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
