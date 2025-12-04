"""期转现-大商所数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesToSpotDceProvider(BaseProvider):
    """期转现-大商所数据提供者"""
    
    collection_name = "futures_to_spot_dce"
    display_name = "期转现-大商所"
    akshare_func = "futures_to_spot_dce"
    unique_keys = ["年月", "品种"]
    
    collection_description = "大连商品交易所期转现数据"
    collection_route = "/futures/collections/futures_to_spot_dce"
    collection_order = 12
    
    param_mapping = {"date": "date"}
    required_params = ["date"]
    add_param_columns = {"date": "年月"}
    
    field_info = [
        {"name": "年月", "type": "string", "description": "年月"},
        {"name": "品种", "type": "string", "description": "品种名称"},
        {"name": "数量", "type": "float", "description": "数量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
