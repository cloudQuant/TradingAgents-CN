"""东财期权行情数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class OptionCurrentEmProvider(BaseProvider):
    """东财期权行情数据提供者"""
    
    collection_name = "option_current_em"
    display_name = "东财期权行情"
    akshare_func = "option_current_em"
    unique_keys = ["品种", "合约代码"]
    
    collection_description = "东方财富网-行情中心-期权市场"
    collection_route = "/options/collections/option_current_em"
    collection_order = 27
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "品种"}
    
    field_info = [
        {"name": "品种", "type": "string", "description": "品种"},
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "合约名称", "type": "string", "description": "合约名称"},
        {"name": "最新价", "type": "float", "description": "最新价"},
        {"name": "涨跌", "type": "float", "description": "涨跌"},
        {"name": "涨跌幅", "type": "float", "description": "涨跌幅"},
        {"name": "成交量", "type": "int", "description": "成交量"},
        {"name": "持仓量", "type": "int", "description": "持仓量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
