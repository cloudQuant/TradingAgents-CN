"""期权实时数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class OptionSseSpotPriceSinaProvider(BaseProvider):
    """期权实时数据提供者"""
    
    collection_name = "option_sse_spot_price_sina"
    display_name = "期权实时数据"
    akshare_func = "option_sse_spot_price_sina"
    unique_keys = ["合约代码"]
    
    collection_description = "期权实时数据"
    collection_route = "/options/collections/option_sse_spot_price_sina"
    collection_order = 20
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "合约代码"}
    
    field_info = [
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "最新价", "type": "float", "description": "最新价"},
        {"name": "涨跌", "type": "float", "description": "涨跌"},
        {"name": "涨跌幅", "type": "float", "description": "涨跌幅"},
        {"name": "成交量", "type": "int", "description": "成交量"},
        {"name": "持仓量", "type": "int", "description": "持仓量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
