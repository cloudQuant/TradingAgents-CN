"""货币报价时间序列数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class CurrencyTimeSeriesProvider(BaseProvider):
    """货币报价时间序列数据提供者"""
    
    collection_name = "currency_time_series"
    display_name = "货币报价时间序列数据"
    akshare_func = "currency_time_series"
    unique_keys = ["date", "base"]
    
    collection_description = "货币报价时间序列数据，返回指定货币在指定日期范围的报价"
    collection_route = "/currencies/collections/currency_time_series"
    collection_order = 3
    
    param_mapping = {
        "base": "base",
        "start_date": "start_date",
        "end_date": "end_date",
        "symbols": "symbols",
        "api_key": "api_key"
    }
    required_params = ["base", "start_date", "end_date", "api_key"]
    add_param_columns = {"base": "base"}
    
    field_info = [
        {"name": "date", "type": "string", "description": "日期"},
        {"name": "base", "type": "string", "description": "基准货币"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
