"""内盘-实时行情数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesZhSpotProvider(BaseProvider):
    """内盘-实时行情数据提供者"""
    
    collection_name = "futures_zh_spot"
    display_name = "内盘-实时行情数据"
    akshare_func = "futures_zh_spot"
    unique_keys = ["symbol"]
    
    collection_description = "内盘期货实时行情数据"
    collection_route = "/futures/collections/futures_zh_spot"
    collection_order = 29
    
    param_mapping = {"market": "subscribe_exchange"}
    required_params = []
    
    field_info = [
        {"name": "symbol", "type": "string", "description": "合约代码"},
        {"name": "name", "type": "string", "description": "合约名称"},
        {"name": "open", "type": "float", "description": "开盘价"},
        {"name": "high", "type": "float", "description": "最高价"},
        {"name": "low", "type": "float", "description": "最低价"},
        {"name": "close", "type": "float", "description": "收盘价"},
        {"name": "volume", "type": "float", "description": "成交量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
