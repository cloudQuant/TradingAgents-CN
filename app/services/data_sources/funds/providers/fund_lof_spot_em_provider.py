"""
LOF实时行情-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundLofSpotEmProvider(SimpleProvider):
    
    """LOF实时行情-东财数据提供者"""

    collection_description = "东方财富网-LOF实时行情数据，包括最新价、涨跌幅、成交量、市值等"
    collection_route = "/funds/collections/fund_lof_spot_em"
    collection_order = 8

    collection_name = "fund_lof_spot_em"
    display_name = "LOF基金实时行情-东财"
    akshare_func = "fund_lof_spot_em"
    unique_keys = ["代码", "更新时间"]

    field_info = [
        {"name": "代码", "type": "string", "description": ""},
        {"name": "最新价", "type": "float", "description": ""},
        {"name": "涨跌额", "type": "float", "description": ""},
        {"name": "涨跌幅", "type": "float", "description": "注意单位: %"},
        {"name": "成交量", "type": "float", "description": ""},
        {"name": "成交额", "type": "float", "description": ""},
        {"name": "开盘价", "type": "float", "description": ""},
        {"name": "最高价", "type": "float", "description": ""},
        {"name": "最低价", "type": "float", "description": ""},
        {"name": "昨收", "type": "float", "description": ""},
        {"name": "换手率", "type": "float", "description": ""},
        {"name": "流通市值", "type": "int", "description": ""},
        {"name": "总市值", "type": "int", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_lof_spot_em"},
    ]
