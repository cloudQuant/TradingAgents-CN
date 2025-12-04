"""交割配对-郑商所数据提供者"""
from app.services.data_sources.base_provider import SimpleProvider


class FuturesDeliveryMatchCzceProvider(SimpleProvider):
    """交割配对-郑商所数据提供者"""
    
    collection_name = "futures_delivery_match_czce"
    display_name = "交割配对-郑商所"
    akshare_func = "futures_delivery_match_czce"
    unique_keys = ["年份", "品种"]
    
    collection_description = "郑州商品交易所交割配对数据"
    collection_route = "/futures/collections/futures_delivery_match_czce"
    collection_order = 19
    
    field_info = [
        {"name": "年份", "type": "string", "description": "年份"},
        {"name": "品种", "type": "string", "description": "品种名称"},
        {"name": "配对数量", "type": "float", "description": "配对数量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
