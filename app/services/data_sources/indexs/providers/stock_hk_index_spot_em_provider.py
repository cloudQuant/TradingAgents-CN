"""港股指数实时行情-东财数据提供者"""
from app.services.data_sources.base_provider import SimpleProvider


class StockHkIndexSpotEmProvider(SimpleProvider):
    """港股指数实时行情-东财数据提供者"""
    
    collection_name = "stock_hk_index_spot_em"
    display_name = "港股指数实时行情-东财"
    akshare_func = "stock_hk_index_spot_em"
    unique_keys = ["代码"]
    
    collection_description = "东方财富网-行情中心-港股指数实时行情"
    collection_route = "/indexs/collections/stock_hk_index_spot_em"
    collection_order = 12
    
    field_info = [
        {"name": "序号", "type": "int", "description": ""},
        {"name": "内部编号", "type": "int", "description": ""},
        {"name": "代码", "type": "string", "description": "指数代码"},
        {"name": "名称", "type": "string", "description": "指数名称"},
        {"name": "最新价", "type": "float", "description": ""},
        {"name": "涨跌额", "type": "float", "description": ""},
        {"name": "涨跌幅", "type": "float", "description": "注意单位: %"},
        {"name": "今开", "type": "float", "description": ""},
        {"name": "最高", "type": "float", "description": ""},
        {"name": "最低", "type": "float", "description": ""},
        {"name": "昨收", "type": "float", "description": ""},
        {"name": "成交量", "type": "float", "description": ""},
        {"name": "成交额", "type": "float", "description": "注意单位: 港元"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
