"""
货币型基金排行-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundMoneyRankEmProvider(SimpleProvider):
    """货币型基金排行-东财数据提供者"""
    
    collection_name = "fund_money_rank_em"
    display_name = "货币型基金排行-东财"
    akshare_func = "fund_money_rank_em"
    unique_keys = ["基金代码", "日期"]

    field_info = [
        {"name": "序号", "type": "string", "description": ""},
        {"name": "基金代码", "type": "string", "description": ""},
        {"name": "基金简称", "type": "string", "description": ""},
        {"name": "日期", "type": "string", "description": ""},
        {"name": "万份收益", "type": "string", "description": ""},
        {"name": "年化收益率7日", "type": "string", "description": ""},
        {"name": "年化收益率14日", "type": "string", "description": ""},
        {"name": "年化收益率28日", "type": "string", "description": ""},
        {"name": "近1月", "type": "string", "description": ""},
        {"name": "近3月", "type": "string", "description": ""},
        {"name": "近6月", "type": "string", "description": ""},
        {"name": "近1年", "type": "string", "description": ""},
        {"name": "近2年", "type": "string", "description": ""},
        {"name": "近3年", "type": "string", "description": ""},
        {"name": "近5年", "type": "string", "description": ""},
        {"name": "今年来", "type": "string", "description": ""},
        {"name": "成立来", "type": "string", "description": ""},
        {"name": "手续费", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_money_rank_em"},
    ]
