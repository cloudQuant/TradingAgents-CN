"""外盘-实时行情数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesForeignCommodityRealtimeProvider(BaseProvider):
    """外盘-实时行情数据提供者"""
    
    collection_name = "futures_foreign_commodity_realtime"
    display_name = "外盘-实时行情数据"
    akshare_func = "futures_foreign_commodity_realtime"
    unique_keys = ["品种"]
    
    collection_description = "外盘期货实时行情数据"
    collection_route = "/futures/collections/futures_foreign_commodity_realtime"
    collection_order = 36
    
    param_mapping = {"symbol": "subscribe_exchange"}
    required_params = ["symbol"]
    
    field_info = [
        {"name": "品种", "type": "string", "description": "品种名称"},
        {"name": "最新价", "type": "float", "description": "最新价"},
        {"name": "涨跌", "type": "float", "description": "涨跌"},
        {"name": "涨跌幅", "type": "float", "description": "涨跌幅"},
        {"name": "开盘价", "type": "float", "description": "开盘价"},
        {"name": "最高价", "type": "float", "description": "最高价"},
        {"name": "最低价", "type": "float", "description": "最低价"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
