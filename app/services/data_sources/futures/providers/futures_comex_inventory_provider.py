"""COMEX库存数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesComexInventoryProvider(BaseProvider):
    """COMEX库存数据提供者"""
    
    collection_name = "futures_comex_inventory"
    display_name = "COMEX库存数据"
    akshare_func = "futures_comex_inventory"
    unique_keys = ["品种", "日期"]
    
    collection_description = "COMEX库存数据"
    collection_route = "/futures/collections/futures_comex_inventory"
    collection_order = 47
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "品种"}
    
    field_info = [
        {"name": "品种", "type": "string", "description": "品种名称"},
        {"name": "日期", "type": "string", "description": "日期"},
        {"name": "库存", "type": "float", "description": "库存量"},
        {"name": "增减", "type": "float", "description": "增减量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
