"""
京 A 股数据提供者

东方财富网-京 A 股-实时行情数据
接口: stock_bj_a_spot_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockBjASpotEmProvider(SimpleProvider):
    """京 A 股数据提供者"""
    
    # 必填属性
    collection_name = "stock_bj_a_spot_em"
    display_name = "京 A 股"
    akshare_func = "stock_bj_a_spot_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-京 A 股-实时行情数据"
    collection_route = "/stocks/collections/stock_bj_a_spot_em"
    collection_category = "实时行情"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "涨跌额", "type": "float64", "description": "-"},
        {"name": "成交量", "type": "float64", "description": "注意单位: 手"},
        {"name": "成交额", "type": "float64", "description": "注意单位: 元"},
        {"name": "振幅", "type": "float64", "description": "注意单位: %"},
        {"name": "最高", "type": "float64", "description": "-"},
        {"name": "最低", "type": "float64", "description": "-"},
        {"name": "今开", "type": "float64", "description": "-"},
        {"name": "昨收", "type": "float64", "description": "-"},
        {"name": "量比", "type": "float64", "description": "-"},
        {"name": "换手率", "type": "float64", "description": "注意单位: %"},
        {"name": "市盈率-动态", "type": "float64", "description": "-"},
        {"name": "市净率", "type": "float64", "description": "-"},
        {"name": "总市值", "type": "float64", "description": "注意单位: 元"},
        {"name": "流通市值", "type": "float64", "description": "注意单位: 元"},
        {"name": "涨速", "type": "float64", "description": "-"},
        {"name": "5分钟涨跌", "type": "float64", "description": "注意单位: %"},
        {"name": "60日涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "年初至今涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
