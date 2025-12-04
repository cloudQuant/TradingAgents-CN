"""
大盘拥挤度数据提供者

乐咕乐股-大盘拥挤度
接口: stock_a_congestion_lg
"""
from app.services.data_sources.base_provider import SimpleProvider


class StockACongestionLgProvider(SimpleProvider):
    """大盘拥挤度数据提供者"""
    
    # 必填属性
    collection_name = "stock_a_congestion_lg"
    display_name = "大盘拥挤度"
    akshare_func = "stock_a_congestion_lg"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "乐咕乐股-大盘拥挤度"
    collection_route = "/stocks/collections/stock_a_congestion_lg"
    collection_category = "默认"

    # 字段信息
    field_info = [
        {"name": "date", "type": "object", "description": "日期"},
        {"name": "close", "type": "float64", "description": "收盘价"},
        {"name": "congestion", "type": "float64", "description": "拥挤度"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
