"""外盘-品种代码表提供者"""
from app.services.data_sources.base_provider import SimpleProvider


class FuturesHqSubscribeExchangeSymbolProvider(SimpleProvider):
    """外盘-品种代码表提供者"""
    
    collection_name = "futures_hq_subscribe_exchange_symbol"
    display_name = "外盘-品种代码表"
    akshare_func = "futures_hq_subscribe_exchange_symbol"
    unique_keys = ["symbol"]
    
    collection_description = "外盘期货品种代码表"
    collection_route = "/futures/collections/futures_hq_subscribe_exchange_symbol"
    collection_order = 35
    
    field_info = [
        {"name": "symbol", "type": "string", "description": "品种代码"},
        {"name": "name", "type": "string", "description": "品种名称"},
        {"name": "exchange", "type": "string", "description": "交易所"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
