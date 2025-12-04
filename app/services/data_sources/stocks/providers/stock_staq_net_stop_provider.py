"""
两网及退市数据提供者

东方财富网-行情中心-沪深个股-两网及退市
接口: stock_staq_net_stop
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockStaqNetStopProvider(SimpleProvider):
    """两网及退市数据提供者"""
    
    # 必填属性
    collection_name = "stock_staq_net_stop"
    display_name = "两网及退市"
    akshare_func = "stock_staq_net_stop"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富网-行情中心-沪深个股-两网及退市"
    collection_route = "/stocks/collections/stock_staq_net_stop"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "序号", "type": "int64", "description": "-"},
        {"name": "代码", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
