"""
实时行情数据-东财数据提供者

东方财富网-美股-实时行情
接口: stock_us_spot_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockUsSpotEmProvider(SimpleProvider):
    """实时行情数据-东财数据提供者"""
    
    # 必填属性
    collection_name = "stock_us_spot_em"
    display_name = "实时行情数据-东财"
    akshare_func = "stock_us_spot_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-美股-实时行情"
    collection_route = "/stocks/collections/stock_us_spot_em"
    collection_category = "实时行情"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "注意单位: 美元"},
        {"name": "涨跌额", "type": "float64", "description": "注意单位: 美元"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "开盘价", "type": "float64", "description": "注意单位: 美元"},
        {"name": "最高价", "type": "float64", "description": "注意单位: 美元"},
        {"name": "最低价", "type": "float64", "description": "注意单位: 美元"},
        {"name": "昨收价", "type": "float64", "description": "注意单位: 美元"},
        {"name": "总市值", "type": "float64", "description": "注意单位: 美元"},
        {"name": "市盈率", "type": "float64", "description": "-"},
        {"name": "成交量", "type": "float64", "description": "-"},
        {"name": "成交额", "type": "float64", "description": "注意单位: 美元"},
        {"name": "振幅", "type": "float64", "description": "注意单位: %"},
        {"name": "换手率", "type": "float64", "description": "注意单位: %"},
        {"name": "代码", "type": "object", "description": "注意: 用来获取历史数据的代码"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
