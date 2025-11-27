"""
新发基金-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundNewFoundEmProvider(SimpleProvider):
    """新发基金-东财数据提供者"""
    
    collection_name = "fund_new_found_em"
    display_name = "新发基金-东财"
    akshare_func = "fund_new_found_em"
    unique_keys = ["基金代码", "成立日期"]

    field_info = [
        {"name": "基金代码", "type": "string", "description": ""},
        {"name": "基金简称", "type": "string", "description": ""},
        {"name": "发行公司", "type": "string", "description": ""},
        {"name": "基金类型", "type": "string", "description": ""},
        {"name": "集中认购期", "type": "string", "description": ""},
        {"name": "募集份额", "type": "float", "description": "注意单位: 亿份"},
        {"name": "成立日期", "type": "string", "description": ""},
        {"name": "成立来涨幅", "type": "float", "description": "注意单位: %"},
        {"name": "基金经理", "type": "string", "description": ""},
        {"name": "申购状态", "type": "string", "description": ""},
        {"name": "优惠费率", "type": "float", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_new_found_em"},
    ]
