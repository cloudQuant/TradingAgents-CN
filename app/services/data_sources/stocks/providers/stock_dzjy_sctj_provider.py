"""
市场统计数据提供者

东方财富网-数据中心-大宗交易-市场统计
接口: stock_dzjy_sctj
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockDzjySctjProvider(SimpleProvider):
    """市场统计数据提供者"""
    
    # 必填属性
    collection_name = "stock_dzjy_sctj"
    display_name = "市场统计"
    akshare_func = "stock_dzjy_sctj"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-大宗交易-市场统计"
    collection_route = "/stocks/collections/stock_dzjy_sctj"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "交易日期", "type": "object", "description": "-"},
        {"name": "上证指数", "type": "float64", "description": "-"},
        {"name": "上证指数涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "大宗交易成交总额", "type": "float64", "description": "注意单位: 元"},
        {"name": "溢价成交总额", "type": "float64", "description": "注意单位: 元"},
        {"name": "溢价成交总额占比", "type": "float64", "description": "注意单位: %"},
        {"name": "折价成交总额", "type": "float64", "description": "注意单位: 元"},
        {"name": "折价成交总额占比", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
