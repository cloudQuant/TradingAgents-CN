"""货币基础信息查询提供者"""
from app.services.data_sources.base_provider import BaseProvider


class CurrencyCurrenciesProvider(BaseProvider):
    """货币基础信息查询提供者"""
    
    collection_name = "currency_currencies"
    display_name = "货币基础信息查询"
    akshare_func = "currency_currencies"
    unique_keys = ["code"]
    
    collection_description = "所有货币的基础信息，包含名称、代码、符号等"
    collection_route = "/currencies/collections/currency_currencies"
    collection_order = 4
    
    param_mapping = {"c_type": "c_type", "api_key": "api_key"}
    required_params = ["c_type", "api_key"]
    add_param_columns = {"c_type": "货币类型"}
    
    field_info = [
        {"name": "id", "type": "int", "description": "ID"},
        {"name": "name", "type": "string", "description": "货币名称"},
        {"name": "short_code", "type": "string", "description": "简码"},
        {"name": "code", "type": "string", "description": "代码"},
        {"name": "precision", "type": "int", "description": "精度"},
        {"name": "subunit", "type": "int", "description": "子单位"},
        {"name": "symbol", "type": "string", "description": "符号"},
        {"name": "symbol_first", "type": "bool", "description": "符号在前"},
        {"name": "decimal_mark", "type": "string", "description": "小数点标记"},
        {"name": "thousands_separator", "type": "string", "description": "千分位分隔符"},
        {"name": "货币类型", "type": "string", "description": "货币类型(fiat/crypto)"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
