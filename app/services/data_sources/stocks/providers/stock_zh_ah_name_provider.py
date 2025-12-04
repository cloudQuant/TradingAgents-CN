"""
A+H股票字典数据提供者

A+H 股数据是从腾讯财经获取的数据, 历史数据按日频率更新
接口: stock_zh_ah_name
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockZhAhNameProvider(SimpleProvider):
    """A+H股票字典数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_ah_name"
    display_name = "A+H股票字典"
    akshare_func = "stock_zh_ah_name"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "A+H 股数据是从腾讯财经获取的数据, 历史数据按日频率更新"
    collection_route = "/stocks/collections/stock_zh_ah_name"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
