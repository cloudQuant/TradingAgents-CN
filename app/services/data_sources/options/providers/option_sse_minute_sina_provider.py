"""期权分钟数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class OptionSseMinuteSinaProvider(BaseProvider):
    """期权分钟数据提供者"""
    
    collection_name = "option_sse_minute_sina"
    display_name = "期权分钟数据"
    akshare_func = "option_sse_minute_sina"
    unique_keys = ["合约代码", "时间"]
    
    collection_description = "期权行情分钟数据，只能返还当天的分钟数据"
    collection_route = "/options/collections/option_sse_minute_sina"
    collection_order = 23
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "合约代码"}
    
    field_info = [
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "时间", "type": "string", "description": "时间"},
        {"name": "开盘", "type": "float", "description": "开盘价"},
        {"name": "最高", "type": "float", "description": "最高价"},
        {"name": "最低", "type": "float", "description": "最低价"},
        {"name": "收盘", "type": "float", "description": "收盘价"},
        {"name": "成交量", "type": "int", "description": "成交量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
