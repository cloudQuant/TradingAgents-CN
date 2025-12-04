"""外盘-历史行情数据-东财提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesGlobalHistEmProvider(BaseProvider):
    """外盘-历史行情数据-东财提供者"""
    
    collection_name = "futures_global_hist_em"
    display_name = "外盘-历史行情数据-东财"
    akshare_func = "futures_global_hist_em"
    unique_keys = ["symbol", "日期"]
    
    collection_description = "外盘期货历史行情数据(东方财富)"
    collection_route = "/futures/collections/futures_global_hist_em"
    collection_order = 38
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "合约代码"}
    
    field_info = [
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "日期", "type": "string", "description": "日期"},
        {"name": "开盘", "type": "float", "description": "开盘价"},
        {"name": "最高", "type": "float", "description": "最高价"},
        {"name": "最低", "type": "float", "description": "最低价"},
        {"name": "收盘", "type": "float", "description": "收盘价"},
        {"name": "成交量", "type": "float", "description": "成交量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
