"""货币报价历史数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class CurrencyHistoryProvider(BaseProvider):
    """货币报价历史数据提供者"""
    
    collection_name = "currency_history"
    display_name = "货币报价历史数据"
    akshare_func = "currency_history"
    unique_keys = ["currency", "base", "date"]
    
    collection_description = "货币报价历史数据，返回指定货币在指定交易日的报价"
    collection_route = "/currencies/collections/currency_history"
    collection_order = 2
    
    param_mapping = {"base": "base", "date": "date", "symbols": "symbols", "api_key": "api_key"}
    required_params = ["base", "date", "api_key"]
    add_param_columns = {"base": "base", "date": "查询日期"}
    
    field_info = [
        {"name": "currency", "type": "string", "description": "货币代码"},
        {"name": "date", "type": "string", "description": "日期"},
        {"name": "base", "type": "string", "description": "基准货币"},
        {"name": "rates", "type": "float", "description": "汇率"},
        {"name": "查询日期", "type": "string", "description": "查询日期"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
