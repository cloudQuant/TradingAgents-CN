"""
基金业绩表现-雪球数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundIndividualAchievementXqProvider(SimpleProvider):
    """基金业绩表现-雪球数据提供者"""
    
    collection_name = "fund_individual_achievement_xq"
    display_name = "基金业绩表现-雪球"
    akshare_func = "fund_individual_achievement_xq"
    unique_keys = ["更新时间"]

    field_info = [
        {"name": "业绩类型", "type": "string", "description": ""},
        {"name": "周期", "type": "string", "description": ""},
        {"name": "本产品区间收益", "type": "float", "description": "注意单位: %"},
        {"name": "本产品最大回撒", "type": "float", "description": "注意单位: %"},
        {"name": "周期收益同类排名", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_individual_achievement_xq"},
    ]
