"""
增发数据提供者

东方财富网-数据中心-新股数据-增发-全部增发
接口: stock_qbzf_em
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockQbzfEmProvider(SimpleProvider):
    """增发数据提供者"""
    
    # 必填属性
    collection_name = "stock_qbzf_em"
    display_name = "增发"
    akshare_func = "stock_qbzf_em"
    unique_keys = ['股票代码']
    
    # 可选属性
    collection_description = "东方财富网-数据中心-新股数据-增发-全部增发"
    collection_route = "/stocks/collections/stock_qbzf_em"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "股票代码", "type": "object", "description": "-"},
        {"name": "股票简称", "type": "object", "description": "-"},
        {"name": "增发代码", "type": "object", "description": "-"},
        {"name": "发行方式", "type": "object", "description": "-"},
        {"name": "发行总数", "type": "int64", "description": "注意单位: 股"},
        {"name": "网上发行", "type": "object", "description": "注意单位: 股"},
        {"name": "发行价格", "type": "float64", "description": "-"},
        {"name": "最新价", "type": "float64", "description": "-"},
        {"name": "发行日期", "type": "object", "description": "-"},
        {"name": "增发上市日期", "type": "object", "description": "-"},
        {"name": "锁定期", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
