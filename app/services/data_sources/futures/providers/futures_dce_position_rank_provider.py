"""大连商品交易所-持仓排名数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class FuturesDcePositionRankProvider(BaseProvider):
    """大连商品交易所-持仓排名数据提供者"""
    
    collection_name = "futures_dce_position_rank"
    display_name = "大连商品交易所-持仓排名"
    akshare_func = "futures_dce_position_rank"
    unique_keys = ["日期", "品种", "会员名称", "排名"]
    
    collection_description = "大连商品交易所期货持仓排名数据"
    collection_route = "/futures/collections/futures_dce_position_rank"
    collection_order = 6
    
    param_mapping = {"date": "date"}
    required_params = ["date"]
    add_param_columns = {"date": "日期"}
    
    field_info = [
        {"name": "日期", "type": "string", "description": "交易日期"},
        {"name": "品种", "type": "string", "description": "品种名称"},
        {"name": "合约", "type": "string", "description": "合约代码"},
        {"name": "排名", "type": "int", "description": "排名"},
        {"name": "会员名称", "type": "string", "description": "会员名称"},
        {"name": "成交量", "type": "float", "description": "成交量"},
        {"name": "增减", "type": "float", "description": "成交量增减"},
        {"name": "持买仓量", "type": "float", "description": "持买仓量"},
        {"name": "持买仓增减", "type": "float", "description": "持买仓增减"},
        {"name": "持卖仓量", "type": "float", "description": "持卖仓量"},
        {"name": "持卖仓增减", "type": "float", "description": "持卖仓增减"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
