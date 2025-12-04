"""现货与股票提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesSpotStockProvider(BaseProvider):
    """现货与股票提供者"""
    
    collection_name = "futures_spot_stock"
    display_name = "现货与股票"
    akshare_func = "futures_spot_stock"
    unique_keys = ["品种", "日期"]
    
    collection_description = "现货与股票对比数据"
    collection_route = "/futures/collections/futures_spot_stock"
    collection_order = 46
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "品种"}
    
    field_info = [
        {"name": "品种", "type": "string", "description": "品种名称"},
        {"name": "日期", "type": "string", "description": "日期"},
        {"name": "现货价格", "type": "float", "description": "现货价格"},
        {"name": "股票价格", "type": "float", "description": "股票价格"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
