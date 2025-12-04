"""期货合约详情-东财提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesContractDetailEmProvider(BaseProvider):
    """期货合约详情-东财提供者"""
    
    collection_name = "futures_contract_detail_em"
    display_name = "期货合约详情-东财"
    akshare_func = "futures_contract_detail_em"
    unique_keys = ["symbol"]
    
    collection_description = "期货合约详情(东方财富)"
    collection_route = "/futures/collections/futures_contract_detail_em"
    collection_order = 44
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "合约代码"}
    
    field_info = [
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "合约名称", "type": "string", "description": "合约名称"},
        {"name": "交易单位", "type": "string", "description": "交易单位"},
        {"name": "最小变动价位", "type": "string", "description": "最小变动价位"},
        {"name": "交易时间", "type": "string", "description": "交易时间"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
