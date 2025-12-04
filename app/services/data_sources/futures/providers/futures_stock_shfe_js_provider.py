"""上海期货交易所-库存数据提供者"""
from app.services.data_sources.base_provider import SimpleProvider


class FuturesStockShfeJsProvider(SimpleProvider):
    """上海期货交易所-库存数据(金十)提供者"""
    
    collection_name = "futures_stock_shfe_js"
    display_name = "上海期货交易所-库存数据"
    akshare_func = "futures_stock_shfe_js"
    unique_keys = ["日期", "品种"]
    
    collection_description = "上海期货交易所库存数据(金十)"
    collection_route = "/futures/collections/futures_stock_shfe_js"
    collection_order = 20
    
    field_info = [
        {"name": "日期", "type": "string", "description": "日期"},
        {"name": "品种", "type": "string", "description": "品种名称"},
        {"name": "库存", "type": "float", "description": "库存量"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
