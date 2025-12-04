"""
实时行情数据-新浪数据提供者

B 股数据是从新浪财经获取的数据, 重复运行本函数会被新浪暂时封 IP, 建议增加时间间隔
接口: stock_zh_b_spot
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockZhBSpotProvider(SimpleProvider):
    """实时行情数据-新浪数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_b_spot"
    display_name = "实时行情数据-新浪"
    akshare_func = "stock_zh_b_spot"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "B 股数据是从新浪财经获取的数据, 重复运行本函数会被新浪暂时封 IP, 建议增加时间间隔"
    collection_route = "/stocks/collections/stock_zh_b_spot"
    collection_category = "实时行情"

    # 字段信息
    field_info = [
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "涨跌额", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "买入", "type": "float64", "description": "-"},
        {"name": "卖出", "type": "float64", "description": "-"},
        {"name": "昨收", "type": "float64", "description": "-"},
        {"name": "今开", "type": "float64", "description": "-"},
        {"name": "最高", "type": "float64", "description": "-"},
        {"name": "最低", "type": "float64", "description": "-"},
        {"name": "成交量", "type": "float64", "description": "注意单位: 股"},
        {"name": "成交额", "type": "float64", "description": "注意单位: 元"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
