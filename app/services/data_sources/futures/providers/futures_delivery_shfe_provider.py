"""交割统计-上期所数据提供者"""
from app.services.data_sources.base_provider import SimpleProvider


class FuturesDeliveryShfeProvider(SimpleProvider):
    """交割统计-上期所数据提供者"""
    
    collection_name = "futures_delivery_shfe"
    display_name = "交割统计-上期所"
    akshare_func = "futures_delivery_shfe"
    unique_keys = ["年份", "品种"]
    
    collection_description = "上海期货交易所交割统计数据"
    collection_route = "/futures/collections/futures_delivery_shfe"
    collection_order = 17
    
    field_info = [
        {"name": "年份", "type": "string", "description": "年份"},
        {"name": "品种", "type": "string", "description": "品种名称"},
        {"name": "交割量", "type": "float", "description": "交割量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
