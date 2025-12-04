"""广期所期权数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class OptionHistGfexProvider(BaseProvider):
    """广期所期权数据提供者"""
    
    collection_name = "option_hist_gfex"
    display_name = "广期所期权数据"
    akshare_func = "option_hist_gfex"
    unique_keys = ["品种", "日期", "合约代码"]
    
    collection_description = "广州期货交易所商品期权数据"
    collection_route = "/options/collections/option_hist_gfex"
    collection_order = 40
    
    param_mapping = {"symbol": "symbol", "date": "date"}
    required_params = ["symbol", "date"]
    add_param_columns = {"symbol": "品种", "date": "日期"}
    
    field_info = [
        {"name": "品种", "type": "string", "description": "品种"},
        {"name": "日期", "type": "string", "description": "日期"},
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "开盘", "type": "float", "description": "开盘价"},
        {"name": "最高", "type": "float", "description": "最高价"},
        {"name": "最低", "type": "float", "description": "最低价"},
        {"name": "收盘", "type": "float", "description": "收盘价"},
        {"name": "结算价", "type": "float", "description": "结算价"},
        {"name": "成交量", "type": "int", "description": "成交量"},
        {"name": "持仓量", "type": "int", "description": "持仓量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
