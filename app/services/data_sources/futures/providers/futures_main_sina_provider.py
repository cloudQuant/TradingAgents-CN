"""期货连续合约-新浪提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesMainSinaProvider(BaseProvider):
    """期货连续合约-新浪提供者"""
    
    collection_name = "futures_main_sina"
    display_name = "期货连续合约-新浪"
    akshare_func = "futures_main_sina"
    unique_keys = ["symbol", "date"]
    
    collection_description = "期货连续合约数据(新浪)"
    collection_route = "/futures/collections/futures_main_sina"
    collection_order = 42
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "品种代码"}
    
    field_info = [
        {"name": "品种代码", "type": "string", "description": "品种代码"},
        {"name": "date", "type": "string", "description": "日期"},
        {"name": "open", "type": "float", "description": "开盘价"},
        {"name": "high", "type": "float", "description": "最高价"},
        {"name": "low", "type": "float", "description": "最低价"},
        {"name": "close", "type": "float", "description": "收盘价"},
        {"name": "volume", "type": "float", "description": "成交量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
