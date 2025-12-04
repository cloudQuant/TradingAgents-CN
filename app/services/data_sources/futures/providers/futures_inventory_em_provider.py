"""库存数据-东方财富数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesInventoryEmProvider(BaseProvider):
    """库存数据-东方财富数据提供者"""
    
    collection_name = "futures_inventory_em"
    display_name = "库存数据-东方财富"
    akshare_func = "futures_inventory_em"
    unique_keys = ["symbol", "日期"]
    
    collection_description = "东方财富期货库存数据"
    collection_route = "/futures/collections/futures_inventory_em"
    collection_order = 5
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "品种代码"}
    
    field_info = [
        {"name": "品种代码", "type": "string", "description": "品种代码"},
        {"name": "日期", "type": "string", "description": "日期"},
        {"name": "库存", "type": "float", "description": "库存量"},
        {"name": "增减", "type": "float", "description": "库存增减"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
