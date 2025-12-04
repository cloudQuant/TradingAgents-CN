"""货币对价格转换提供者"""
from app.services.data_sources.base_provider import BaseProvider


class CurrencyConvertProvider(BaseProvider):
    """货币对价格转换提供者"""
    
    collection_name = "currency_convert"
    display_name = "货币对价格转换"
    akshare_func = "currency_convert"
    unique_keys = ["from", "to", "timestamp"]
    
    collection_description = "指定货币对指定货币数量的转换后价格"
    collection_route = "/currencies/collections/currency_convert"
    collection_order = 5
    
    param_mapping = {"base": "base", "to": "to", "amount": "amount", "api_key": "api_key"}
    required_params = ["base", "to", "amount", "api_key"]
    add_param_columns = {}
    
    field_info = [
        {"name": "item", "type": "string", "description": "项目"},
        {"name": "value", "type": "string", "description": "值"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
