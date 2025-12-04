"""期权标的物实时数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class OptionSseUnderlyingSpotPriceSinaProvider(BaseProvider):
    """期权标的物实时数据提供者"""
    
    collection_name = "option_sse_underlying_spot_price_sina"
    display_name = "期权标的物实时数据"
    akshare_func = "option_sse_underlying_spot_price_sina"
    unique_keys = ["品种"]
    
    collection_description = "获取期权标的物的实时数据"
    collection_route = "/options/collections/option_sse_underlying_spot_price_sina"
    collection_order = 21
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "品种"}
    
    field_info = [
        {"name": "品种", "type": "string", "description": "品种"},
        {"name": "最新价", "type": "float", "description": "最新价"},
        {"name": "涨跌", "type": "float", "description": "涨跌"},
        {"name": "涨跌幅", "type": "float", "description": "涨跌幅"},
        {"name": "成交量", "type": "int", "description": "成交量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
