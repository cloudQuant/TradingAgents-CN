"""广州期货交易所-持仓排名数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesGfexPositionRankProvider(BaseProvider):
    """广州期货交易所-持仓排名数据提供者"""
    
    collection_name = "futures_gfex_position_rank"
    display_name = "广州期货交易所-持仓排名"
    akshare_func = "futures_gfex_position_rank"
    unique_keys = ["日期", "品种", "会员简称", "名次"]
    
    collection_description = "广州期货交易所期货持仓排名数据"
    collection_route = "/futures/collections/futures_gfex_position_rank"
    collection_order = 7
    
    param_mapping = {"date": "date"}
    required_params = ["date"]
    add_param_columns = {"date": "日期"}
    
    field_info = [
        {"name": "日期", "type": "string", "description": "交易日期"},
        {"name": "品种", "type": "string", "description": "品种名称"},
        {"name": "名次", "type": "int", "description": "排名"},
        {"name": "会员简称", "type": "string", "description": "会员简称"},
        {"name": "成交量", "type": "float", "description": "成交量"},
        {"name": "成交量增减", "type": "float", "description": "成交量增减"},
        {"name": "持买单量", "type": "float", "description": "持买单量"},
        {"name": "持买单量增减", "type": "float", "description": "持买单量增减"},
        {"name": "持卖单量", "type": "float", "description": "持卖单量"},
        {"name": "持卖单量增减", "type": "float", "description": "持卖单量增减"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
