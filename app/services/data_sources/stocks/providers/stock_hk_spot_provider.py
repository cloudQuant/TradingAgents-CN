"""
实时行情数据-新浪数据提供者

获取所有港股的实时行情数据 15 分钟延时
接口: stock_hk_spot
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockHkSpotProvider(SimpleProvider):
    """实时行情数据-新浪数据提供者"""
    
    # 必填属性
    collection_name = "stock_hk_spot"
    display_name = "实时行情数据-新浪"
    akshare_func = "stock_hk_spot"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "获取所有港股的实时行情数据 15 分钟延时"
    collection_route = "/stocks/collections/stock_hk_spot"
    collection_category = "实时行情"

    # 字段信息
    field_info = [
        {"name": "日期时间", "type": "object", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "交易类型", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "涨跌额", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "-"},
        {"name": "昨收", "type": "float64", "description": "-"},
        {"name": "今开", "type": "float64", "description": "-"},
        {"name": "最高", "type": "float64", "description": "-"},
        {"name": "最低", "type": "float64", "description": "-"},
        {"name": "成交量", "type": "float64", "description": "-"},
        {"name": "成交额", "type": "float64", "description": "-"},
        {"name": "买一", "type": "float64", "description": "-"},
        {"name": "卖一", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
