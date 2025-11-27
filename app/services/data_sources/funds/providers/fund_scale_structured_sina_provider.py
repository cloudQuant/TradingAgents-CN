"""
分级基金规模-新浪数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundScaleStructuredSinaProvider(SimpleProvider):
    """分级基金规模-新浪数据提供者"""
    
    collection_name = "fund_scale_structured_sina"
    display_name = "分级基金规模-新浪"
    akshare_func = "fund_scale_structured_sina"
    unique_keys = ["基金代码", "成立日期"]

    field_info = [
        {"name": "序号", "type": "int", "description": ""},
        {"name": "基金代码", "type": "string", "description": ""},
        {"name": "基金简称", "type": "string", "description": ""},
        {"name": "单位净值", "type": "float", "description": "注意单位: 元"},
        {"name": "总募集规模", "type": "float", "description": "注意单位: 万份"},
        {"name": "最近总份额", "type": "float", "description": "注意单位: 份"},
        {"name": "成立日期", "type": "string", "description": ""},
        {"name": "基金经理", "type": "string", "description": ""},
        {"name": "更新日期", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_scale_structured_sina"},
    ]
