"""看涨看跌合约代码数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class OptionSseCodesSinaProvider(BaseProvider):
    """看涨看跌合约代码数据提供者"""
    
    collection_name = "option_sse_codes_sina"
    display_name = "看涨看跌合约代码"
    akshare_func = "option_sse_codes_sina"
    unique_keys = ["到期月份", "品种", "合约代码"]
    
    collection_description = "新浪期权看涨看跌合约的代码"
    collection_route = "/options/collections/option_sse_codes_sina"
    collection_order = 19
    
    param_mapping = {"trade_date": "trade_date", "underlying": "underlying"}
    required_params = ["trade_date", "underlying"]
    add_param_columns = {"trade_date": "到期月份", "underlying": "品种"}
    
    field_info = [
        {"name": "到期月份", "type": "string", "description": "到期月份"},
        {"name": "品种", "type": "string", "description": "品种"},
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "类型", "type": "string", "description": "看涨/看跌"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
