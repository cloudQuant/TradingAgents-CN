"""外盘-实时行情数据-东财提供者"""
from app.services.data_sources.base_provider import SimpleProvider


class FuturesGlobalSpotEmProvider(SimpleProvider):
    """外盘-实时行情数据-东财提供者"""
    
    collection_name = "futures_global_spot_em"
    display_name = "外盘-实时行情数据-东财"
    akshare_func = "futures_global_spot_em"
    unique_keys = ["代码"]
    
    collection_description = "外盘期货实时行情数据(东方财富)"
    collection_route = "/futures/collections/futures_global_spot_em"
    collection_order = 37
    
    field_info = [
        {"name": "代码", "type": "string", "description": "合约代码"},
        {"name": "名称", "type": "string", "description": "合约名称"},
        {"name": "最新价", "type": "float", "description": "最新价"},
        {"name": "涨跌额", "type": "float", "description": "涨跌额"},
        {"name": "涨跌幅", "type": "float", "description": "涨跌幅"},
        {"name": "开盘价", "type": "float", "description": "开盘价"},
        {"name": "最高价", "type": "float", "description": "最高价"},
        {"name": "最低价", "type": "float", "description": "最低价"},
        {"name": "昨结算", "type": "float", "description": "昨结算"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
