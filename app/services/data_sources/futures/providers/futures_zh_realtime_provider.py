"""内盘-实时行情数据(品种)提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesZhRealtimeProvider(BaseProvider):
    """内盘-实时行情数据(品种)提供者"""
    
    collection_name = "futures_zh_realtime"
    display_name = "内盘-实时行情数据(品种)"
    akshare_func = "futures_zh_realtime"
    unique_keys = ["symbol"]
    
    collection_description = "内盘期货实时行情数据(按品种)"
    collection_route = "/futures/collections/futures_zh_realtime"
    collection_order = 30
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "品种"}
    
    field_info = [
        {"name": "品种", "type": "string", "description": "品种名称"},
        {"name": "symbol", "type": "string", "description": "合约代码"},
        {"name": "最新价", "type": "float", "description": "最新价"},
        {"name": "涨跌", "type": "float", "description": "涨跌"},
        {"name": "涨跌幅", "type": "float", "description": "涨跌幅"},
        {"name": "成交量", "type": "float", "description": "成交量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
