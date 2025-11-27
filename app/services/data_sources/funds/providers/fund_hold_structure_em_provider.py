"""
基金持有结构-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundHoldStructureEmProvider(SimpleProvider):
    """基金持有结构-东财数据提供者"""
    
    collection_name = "fund_hold_structure_em"
    display_name = "基金持有结构-东财"
    akshare_func = "fund_hold_structure_em"
    unique_keys = ["截止日期"]

    field_info = [
        {"name": "序号", "type": "int", "description": ""},
        {"name": "截止日期", "type": "string", "description": ""},
        {"name": "基金家数", "type": "int", "description": ""},
        {"name": "机构持有比列", "type": "float", "description": "注意单位: %"},
        {"name": "个人持有比列", "type": "float", "description": "注意单位: %"},
        {"name": "内部持有比列", "type": "float", "description": "注意单位: %"},
        {"name": "总份额", "type": "float", "description": "注意单位: 亿份"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_hold_structure_em"},
    ]
