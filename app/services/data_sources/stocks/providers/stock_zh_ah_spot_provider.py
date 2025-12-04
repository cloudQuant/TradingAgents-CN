"""
实时行情数据-腾讯数据提供者

A+H 股数据是从腾讯财经获取的数据, 延迟 15 分钟更新
接口: stock_zh_ah_spot
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockZhAhSpotProvider(SimpleProvider):
    """实时行情数据-腾讯数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_ah_spot"
    display_name = "实时行情数据-腾讯"
    akshare_func = "stock_zh_ah_spot"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "A+H 股数据是从腾讯财经获取的数据, 延迟 15 分钟更新"
    collection_route = "/stocks/collections/stock_zh_ah_spot"
    collection_category = "实时行情"

    # 字段信息
    field_info = [
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "涨跌额", "type": "float64", "description": "-"},
        {"name": "买入", "type": "float64", "description": "-"},
        {"name": "卖出", "type": "float64", "description": "-"},
        {"name": "成交量", "type": "float64", "description": "-"},
        {"name": "成交额", "type": "float64", "description": "-"},
        {"name": "今开", "type": "float64", "description": "-"},
        {"name": "昨收", "type": "float64", "description": "-"},
        {"name": "最高", "type": "float64", "description": "-"},
        {"name": "最低", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
