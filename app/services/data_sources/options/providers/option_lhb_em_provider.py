"""期权龙虎榜数据提供者"""
from app.services.data_sources.base_provider import BaseProvider


class OptionLhbEmProvider(BaseProvider):
    """期权龙虎榜数据提供者"""
    
    collection_name = "option_lhb_em"
    display_name = "期权龙虎榜"
    akshare_func = "option_lhb_em"
    unique_keys = ["品种", "日期", "排名"]
    
    collection_description = "东方财富网-数据中心-期货期权-期权龙虎榜单-金融期权"
    collection_route = "/options/collections/option_lhb_em"
    collection_order = 28
    
    param_mapping = {"symbol": "symbol"}
    required_params = ["symbol"]
    add_param_columns = {"symbol": "品种"}
    
    field_info = [
        {"name": "品种", "type": "string", "description": "品种"},
        {"name": "日期", "type": "string", "description": "日期"},
        {"name": "排名", "type": "int", "description": "排名"},
        {"name": "会员简称", "type": "string", "description": "会员简称"},
        {"name": "成交量", "type": "int", "description": "成交量"},
        {"name": "增减", "type": "int", "description": "增减"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
