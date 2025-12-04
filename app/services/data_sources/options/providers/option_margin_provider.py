"""期权保证金数据提供者"""
from app.services.data_sources.base_provider import SimpleProvider


class OptionMarginProvider(SimpleProvider):
    """期权保证金数据提供者"""
    
    collection_name = "option_margin"
    display_name = "期权保证金"
    akshare_func = "option_margin"
    unique_keys = ["交易所", "品种"]
    
    collection_description = "唯爱期货-期权保证金"
    collection_route = "/options/collections/option_margin"
    collection_order = 36
    
    field_info = [
        {"name": "交易所", "type": "string", "description": "交易所"},
        {"name": "品种", "type": "string", "description": "品种"},
        {"name": "保证金", "type": "string", "description": "保证金"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
