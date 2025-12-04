"""商品期权T型报价表数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class OptionCommodityContractTableSinaProvider(BaseProvider):
    """商品期权T型报价表数据提供者"""
    
    collection_name = "option_commodity_contract_table_sina"
    display_name = "商品期权T型报价表"
    akshare_func = "option_commodity_contract_table_sina"
    unique_keys = ["品种", "行权价"]
    
    collection_description = "新浪财经-商品期权的T型报价表"
    collection_route = "/options/collections/option_commodity_contract_table_sina"
    collection_order = 33
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "品种"}
    
    field_info = [
        {"name": "品种", "type": "string", "description": "品种"},
        {"name": "行权价", "type": "float", "description": "行权价"},
        {"name": "看涨合约", "type": "string", "description": "看涨合约"},
        {"name": "看跌合约", "type": "string", "description": "看跌合约"},
        {"name": "看涨最新价", "type": "float", "description": "看涨最新价"},
        {"name": "看跌最新价", "type": "float", "description": "看跌最新价"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
