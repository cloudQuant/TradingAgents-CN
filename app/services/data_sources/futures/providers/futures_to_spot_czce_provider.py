"""期转现-郑商所数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesToSpotCzceProvider(BaseProvider):
    """期转现-郑商所数据提供者"""
    
    collection_name = "futures_to_spot_czce"
    display_name = "期转现-郑商所"
    akshare_func = "futures_to_spot_czce"
    unique_keys = ["日期", "品种"]
    
    collection_description = "郑州商品交易所期转现数据"
    collection_route = "/futures/collections/futures_to_spot_czce"
    collection_order = 13
    
    param_mapping = {"date": "date"}
    required_params = ["date"]
    add_param_columns = {"date": "日期"}
    
    field_info = [
        {"name": "日期", "type": "string", "description": "交易日期"},
        {"name": "品种", "type": "string", "description": "品种名称"},
        {"name": "数量", "type": "float", "description": "数量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
