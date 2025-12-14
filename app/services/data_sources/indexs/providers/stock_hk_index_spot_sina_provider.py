"""港股指数实时行情-新浪数据提供者"""
from app.services.data_sources.base_provider import SimpleProvider


class StockHkIndexSpotSinaProvider(SimpleProvider):
    """港股指数实时行情-新浪数据提供者"""
    
    collection_name = "stock_hk_index_spot_sina"
    display_name = "港股指数实时行情-新浪"
    akshare_func = "stock_hk_index_spot_sina"
    unique_keys = ["代码"]
    
    collection_description = "新浪财经-行情中心-港股指数实时行情"
    collection_route = "/indexs/collections/stock_hk_index_spot_sina"
    collection_order = 10
    
    field_info = [
        {"name": "代码", "type": "string", "description": "指数代码"},
        {"name": "名称", "type": "string", "description": "指数名称"},
        {"name": "最新价", "type": "float", "description": ""},
        {"name": "涨跌额", "type": "float", "description": ""},
        {"name": "涨跌幅", "type": "float", "description": "注意单位: %"},
        {"name": "昨收", "type": "float", "description": ""},
        {"name": "今开", "type": "float", "description": ""},
        {"name": "最高", "type": "float", "description": ""},
        {"name": "最低", "type": "float", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
