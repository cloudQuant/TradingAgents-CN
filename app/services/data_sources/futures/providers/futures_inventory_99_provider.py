"""库存数据-99期货网数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesInventory99Provider(BaseProvider):
    """库存数据-99期货网数据提供者"""
    
    collection_name = "futures_inventory_99"
    display_name = "库存数据-99期货网"
    akshare_func = "futures_inventory_99"
    unique_keys = ["symbol", "日期"]
    
    collection_description = "99期货网期货库存数据"
    collection_route = "/futures/collections/futures_inventory_99"
    collection_order = 4
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "品种"}
    
    field_info = [
        {"name": "品种", "type": "string", "description": "品种名称"},
        {"name": "日期", "type": "string", "description": "日期"},
        {"name": "库存", "type": "float", "description": "库存量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
