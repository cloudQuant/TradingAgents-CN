"""广州期货交易所-合约信息数据提供者"""
from app.services.data_sources.base_provider import SimpleProvider


class FuturesContractInfoGfexProvider(SimpleProvider):
    """广州期货交易所-合约信息数据提供者"""
    
    collection_name = "futures_contract_info_gfex"
    display_name = "广州期货交易所-合约信息"
    akshare_func = "futures_contract_info_gfex"
    unique_keys = ["合约代码"]
    
    collection_description = "广州期货交易所合约信息"
    collection_route = "/futures/collections/futures_contract_info_gfex"
    collection_order = 27
    
    field_info = [
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "品种", "type": "string", "description": "品种名称"},
        {"name": "合约乘数", "type": "int", "description": "合约乘数"},
        {"name": "最小变动价位", "type": "float", "description": "最小变动价位"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
