"""中金所中证1000指数日频行情数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class OptionCffexZz1000DailySinaProvider(BaseProvider):
    """中金所中证1000指数日频行情数据提供者"""
    
    collection_name = "option_cffex_zz1000_daily_sina"
    display_name = "中金所中证1000指数日频行情"
    akshare_func = "option_cffex_zz1000_daily_sina"
    unique_keys = ["symbol", "日期"]
    
    collection_description = "中金所中证1000指数指定合约日频行情"
    collection_route = "/options/collections/option_cffex_zz1000_daily_sina"
    collection_order = 16
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "合约代码"}
    
    field_info = [
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "日期", "type": "string", "description": "日期"},
        {"name": "开盘", "type": "float", "description": "开盘价"},
        {"name": "最高", "type": "float", "description": "最高价"},
        {"name": "最低", "type": "float", "description": "最低价"},
        {"name": "收盘", "type": "float", "description": "收盘价"},
        {"name": "成交量", "type": "int", "description": "成交量"},
        {"name": "持仓量", "type": "int", "description": "持仓量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
