"""上海期货交易所-合约信息数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesContractInfoShfeProvider(BaseProvider):
    """上海期货交易所-合约信息数据提供者"""
    
    collection_name = "futures_contract_info_shfe"
    display_name = "上海期货交易所-合约信息"
    akshare_func = "futures_contract_info_shfe"
    unique_keys = ["日期", "合约代码"]
    
    collection_description = "上海期货交易所合约信息"
    collection_route = "/futures/collections/futures_contract_info_shfe"
    collection_order = 23
    
    param_mapping = {"date": "date"}
    required_params = ["date"]
    add_param_columns = {"date": "日期"}
    
    field_info = [
        {"name": "日期", "type": "string", "description": "交易日期"},
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "品种", "type": "string", "description": "品种名称"},
        {"name": "合约乘数", "type": "int", "description": "合约乘数"},
        {"name": "最小变动价位", "type": "float", "description": "最小变动价位"},
        {"name": "涨停板", "type": "float", "description": "涨停板"},
        {"name": "跌停板", "type": "float", "description": "跌停板"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
