"""内盘-分时行情数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesZhMinuteSinaProvider(BaseProvider):
    """内盘-分时行情数据提供者"""
    
    collection_name = "futures_zh_minute_sina"
    display_name = "内盘-分时行情数据"
    akshare_func = "futures_zh_minute_sina"
    unique_keys = ["symbol", "datetime"]
    
    collection_description = "内盘期货分时行情数据(新浪)"
    collection_route = "/futures/collections/futures_zh_minute_sina"
    collection_order = 31
    
    param_mapping = {"symbol": "symbol", "period": "period"}
    required_params = ["symbol", "period"]
    add_param_columns = {"symbol": "合约代码"}
    
    field_info = [
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "datetime", "type": "string", "description": "时间"},
        {"name": "open", "type": "float", "description": "开盘价"},
        {"name": "high", "type": "float", "description": "最高价"},
        {"name": "low", "type": "float", "description": "最低价"},
        {"name": "close", "type": "float", "description": "收盘价"},
        {"name": "volume", "type": "float", "description": "成交量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
