"""
基金规模变动-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundScaleChangeEmProvider(SimpleProvider):
    """基金规模变动-东财数据提供者"""
    
    collection_name = "fund_scale_change_em"
    display_name = "基金规模变动-东财"
    akshare_func = "fund_scale_change_em"
    unique_keys = ["截止日期"]

    field_info = [
        {"name": "序号", "type": "int", "description": ""},
        {"name": "截止日期", "type": "string", "description": ""},
        {"name": "基金家数", "type": "int", "description": ""},
        {"name": "期间申购", "type": "float", "description": "注意单位: 亿份"},
        {"name": "期间赎回", "type": "float", "description": "注意单位: 亿份"},
        {"name": "期末总份额", "type": "float", "description": "注意单位: 亿份"},
        {"name": "期末净资产", "type": "float", "description": "注意单位: 亿份"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_scale_change_em"},
    ]
