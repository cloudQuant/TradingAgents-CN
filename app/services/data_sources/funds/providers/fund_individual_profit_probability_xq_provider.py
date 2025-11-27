"""
基金盈利概率-雪球数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundIndividualProfitProbabilityXqProvider(SimpleProvider):
    """基金盈利概率-雪球数据提供者"""
    
    collection_name = "fund_individual_profit_probability_xq"
    display_name = "基金盈利概率-雪球"
    akshare_func = "fund_individual_profit_probability_xq"
    unique_keys = ["更新时间"]

    field_info = [
        {"name": "持有时长", "type": "string", "description": ""},
        {"name": "盈利概率", "type": "string", "description": ""},
        {"name": "平均收益", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_individual_profit_probability_xq"},
    ]
