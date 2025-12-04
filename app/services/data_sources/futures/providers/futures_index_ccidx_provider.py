"""中证商品指数提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesIndexCcidxProvider(BaseProvider):
    """中证商品指数提供者"""
    
    collection_name = "futures_index_ccidx"
    display_name = "中证商品指数"
    akshare_func = "futures_index_ccidx"
    unique_keys = ["symbol", "日期"]
    
    collection_description = "中证商品指数数据"
    collection_route = "/futures/collections/futures_index_ccidx"
    collection_order = 45
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "指数名称"}
    
    field_info = [
        {"name": "指数名称", "type": "string", "description": "指数名称"},
        {"name": "日期", "type": "string", "description": "日期"},
        {"name": "指数值", "type": "float", "description": "指数值"},
        {"name": "涨跌幅", "type": "float", "description": "涨跌幅"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
