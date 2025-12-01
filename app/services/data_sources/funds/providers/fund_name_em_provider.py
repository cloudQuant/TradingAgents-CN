"""
基金基本信息-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundNameEmProvider(SimpleProvider):
    
    """基金基本信息-东财数据提供者"""

    collection_description = "东方财富网所有基金的基本信息，包括基金代码、简称、类型等"
    collection_route = "/funds/collections/fund_name_em"
    collection_order = 0

    collection_name = "fund_name_em"
    display_name = "基金基本信息"
    akshare_func = "fund_name_em"
    unique_keys = ["基金代码"]

    field_info = [
        {"name": "基金代码", "type": "string", "description": ""},
        {"name": "拼音缩写", "type": "string", "description": ""},
        {"name": "基金简称", "type": "string", "description": ""},
        {"name": "基金类型", "type": "string", "description": ""},
        {"name": "拼音全称", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_name_em"},
    ]
