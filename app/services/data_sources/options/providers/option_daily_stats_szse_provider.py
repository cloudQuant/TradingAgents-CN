"""深交所日度概况数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class OptionDailyStatsSzseProvider(BaseProvider):
    """深交所日度概况数据提供者"""
    
    collection_name = "option_daily_stats_szse"
    display_name = "深交所日度概况"
    akshare_func = "option_daily_stats_szse"
    unique_keys = ["日期"]
    
    collection_description = "深圳证券交易所-市场数据-期权数据-日度概况"
    collection_route = "/options/collections/option_daily_stats_szse"
    collection_order = 7
    
    param_mapping = {"date": "date"}
    required_params = ["date"]
    add_param_columns = {"date": "日期"}
    
    field_info = [
        {"name": "日期", "type": "string", "description": "交易日期"},
        {"name": "成交量", "type": "int", "description": "成交量"},
        {"name": "成交额", "type": "float", "description": "成交额"},
        {"name": "持仓量", "type": "int", "description": "持仓量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
