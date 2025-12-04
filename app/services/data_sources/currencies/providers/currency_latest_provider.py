"""货币报价最新数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class CurrencyLatestProvider(BaseProvider):
    """货币报价最新数据提供者"""
    
    collection_name = "currency_latest"
    display_name = "货币报价最新数据"
    akshare_func = "currency_latest"
    unique_keys = ["currency", "base", "date"]
    
    collection_description = "货币报价最新数据，返回指定货币的最新报价"
    collection_route = "/currencies/collections/currency_latest"
    collection_order = 1
    
    param_mapping = {"base": "base", "symbols": "symbols", "api_key": "api_key"}
    required_params = ["base", "api_key"]
    add_param_columns = {"base": "base"}
    
    field_info = [
        {"name": "currency", "type": "string", "description": "货币代码"},
        {"name": "date", "type": "datetime", "description": "日期时间"},
        {"name": "base", "type": "string", "description": "基准货币"},
        {"name": "rates", "type": "float", "description": "汇率"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
