"""
货币型基金实时行情-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundMoneyFundDailyEmProvider(SimpleProvider):
    """货币型基金实时行情-东财数据提供者"""
    
    collection_name = "fund_money_fund_daily_em"
    display_name = "货币型基金实时行情-东财"
    akshare_func = "fund_money_fund_daily_em"
    unique_keys = ["基金代码", "成立日期"]

    field_info = [
        {"name": "基金代码", "type": "string", "description": ""},
        {"name": "基金简称", "type": "string", "description": ""},
        {"name": "当前交易日-万份收益", "type": "float", "description": ""},
        {"name": "当前交易日-7日年化%", "type": "float", "description": ""},
        {"name": "当前交易日-单位净值", "type": "float", "description": ""},
        {"name": "前一交易日-万份收益", "type": "float", "description": ""},
        {"name": "前一交易日-7日年化%", "type": "float", "description": ""},
        {"name": "前一交易日-单位净值", "type": "float", "description": ""},
        {"name": "日涨幅", "type": "string", "description": ""},
        {"name": "成立日期", "type": "string", "description": ""},
        {"name": "基金经理", "type": "string", "description": ""},
        {"name": "手续费", "type": "string", "description": ""},
        {"name": "可购全部", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_money_fund_daily_em"},
    ]
