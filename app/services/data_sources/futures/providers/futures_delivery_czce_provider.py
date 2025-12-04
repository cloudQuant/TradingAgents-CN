"""交割统计-郑商所数据提供者"""
from app.services.data_sources.base_provider import SimpleProvider


class FuturesDeliveryCzceProvider(SimpleProvider):
    """交割统计-郑商所数据提供者"""
    
    collection_name = "futures_delivery_czce"
    display_name = "交割统计-郑商所"
    akshare_func = "futures_delivery_czce"
    unique_keys = ["年份", "品种"]
    
    collection_description = "郑州商品交易所交割统计数据"
    collection_route = "/futures/collections/futures_delivery_czce"
    collection_order = 16
    
    field_info = [
        {"name": "年份", "type": "string", "description": "年份"},
        {"name": "品种", "type": "string", "description": "品种名称"},
        {"name": "交割量", "type": "float", "description": "交割量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
