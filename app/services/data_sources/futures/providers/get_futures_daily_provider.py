"""内盘-历史行情数据-交易所提供者"""
from app.services.data_sources.base_provider import BaseProvider


class GetFuturesDailyProvider(BaseProvider):
    """内盘-历史行情数据-交易所提供者"""
    
    collection_name = "get_futures_daily"
    display_name = "内盘-历史行情数据-交易所"
    akshare_func = "get_futures_daily"
    unique_keys = ["symbol", "date"]
    
    collection_description = "内盘期货历史行情数据(交易所)"
    collection_route = "/futures/collections/get_futures_daily"
    collection_order = 34
    
    param_mapping = {
        "market": "market",
        "start_date": "start_date",
        "end_date": "end_date"
    }
    required_params = ["market", "start_date", "end_date"]
    
    field_info = [
        {"name": "symbol", "type": "string", "description": "合约代码"},
        {"name": "date", "type": "string", "description": "日期"},
        {"name": "open", "type": "float", "description": "开盘价"},
        {"name": "high", "type": "float", "description": "最高价"},
        {"name": "low", "type": "float", "description": "最低价"},
        {"name": "close", "type": "float", "description": "收盘价"},
        {"name": "volume", "type": "float", "description": "成交量"},
        {"name": "open_interest", "type": "float", "description": "持仓量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
