"""
配股数据提供者

东方财富网-数据中心-新股数据-配股
接口: stock_pg_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockPgEmProvider(SimpleProvider):
    """配股数据提供者"""
    
    # 必填属性
    collection_name = "stock_pg_em"
    display_name = "配股"
    akshare_func = "stock_pg_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-新股数据-配股"
    collection_route = "/stocks/collections/stock_pg_em"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "配售代码", "type": "object", "description": "-"},
        {"name": "配股数量", "type": "int64", "description": "注意单位: 股"},
        {"name": "配股比例", "type": "object", "description": "-"},
        {"name": "配股价", "type": "float64", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "配股前总股本", "type": "int64", "description": "注意单位: 股"},
        {"name": "配股后总股本", "type": "int64", "description": "注意单位: 股"},
        {"name": "股权登记日", "type": "object", "description": "-"},
        {"name": "缴款起始日期", "type": "object", "description": "-"},
        {"name": "缴款截止日期", "type": "object", "description": "-"},
        {"name": "上市日", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
