"""
风险警示板数据提供者

东方财富网-行情中心-沪深个股-风险警示板
接口: stock_zh_a_st_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockZhAStEmProvider(SimpleProvider):
    """风险警示板数据提供者"""
    
    # 必填属性
    collection_name = "stock_zh_a_st_em"
    display_name = "风险警示板"
    akshare_func = "stock_zh_a_st_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-行情中心-沪深个股-风险警示板"
    collection_route = "/stocks/collections/stock_zh_a_st_em"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "涨跌幅", "type": "float64", "description": "注意单位: %"},
        {"name": "涨跌额", "type": "float64", "description": "-"},
        {"name": "成交量", "type": "float64", "description": "-"},
        {"name": "成交额", "type": "float64", "description": "-"},
        {"name": "振幅", "type": "float64", "description": "注意单位: %"},
        {"name": "最高", "type": "float64", "description": "-"},
        {"name": "最低", "type": "float64", "description": "-"},
        {"name": "今开", "type": "float64", "description": "-"},
        {"name": "昨收", "type": "float64", "description": "-"},
        {"name": "量比", "type": "float64", "description": "-"},
        {"name": "换手率", "type": "float64", "description": "注意单位: %"},
        {"name": "市盈率-动态", "type": "float64", "description": "-"},
        {"name": "市净率", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
