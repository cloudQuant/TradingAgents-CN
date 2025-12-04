"""商品期权当前合约数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class OptionCommodityContractSinaProvider(BaseProvider):
    """商品期权当前合约数据提供者"""
    
    collection_name = "option_commodity_contract_sina"
    display_name = "商品期权当前合约"
    akshare_func = "option_commodity_contract_sina"
    unique_keys = ["品种", "合约代码"]
    
    collection_description = "新浪财经-商品期权当前在交易的合约"
    collection_route = "/options/collections/option_commodity_contract_sina"
    collection_order = 32
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "品种"}
    
    field_info = [
        {"name": "品种", "type": "string", "description": "品种"},
        {"name": "合约代码", "type": "string", "description": "合约代码"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
