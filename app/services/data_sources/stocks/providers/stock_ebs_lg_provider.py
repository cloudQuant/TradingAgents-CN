"""
股债利差数据提供者

乐咕乐股-股债利差
接口: stock_ebs_lg
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockEbsLgProvider(SimpleProvider):
    """股债利差数据提供者"""
    
    # 必填属性
    collection_name = "stock_ebs_lg"
    display_name = "股债利差"
    akshare_func = "stock_ebs_lg"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "乐咕乐股-股债利差"
    collection_route = "/stocks/collections/stock_ebs_lg"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "日期", "type": "object", "description": "-"},
        {"name": "沪深300指数", "type": "float64", "description": "-"},
        {"name": "股债利差", "type": "float64", "description": "-"},
        {"name": "股债利差均线", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
