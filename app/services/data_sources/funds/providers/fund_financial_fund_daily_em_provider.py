"""
理财型基金实时行情-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundFinancialFundDailyEmProvider(SimpleProvider):
    """理财型基金实时行情-东财数据提供者"""
    
    collection_name = "fund_financial_fund_daily_em"
    display_name = "理财型基金实时行情-东财"
    akshare_func = "fund_financial_fund_daily_em"
    unique_keys = ["基金代码", "更新时间"]

    field_info = [
        {"name": "序号", "type": "int", "description": ""},
        {"name": "基金代码", "type": "string", "description": ""},
        {"name": "基金简称", "type": "string", "description": ""},
        {"name": "上一期年化收益率", "type": "float", "description": ""},
        {"name": "当前交易日-万份收益", "type": "float", "description": ""},
        {"name": "当前交易日-7日年华", "type": "float", "description": ""},
        {"name": "前一个交易日-万份收益", "type": "float", "description": ""},
        {"name": "前一个交易日-7日年华", "type": "float", "description": ""},
        {"name": "封闭期", "type": "float", "description": ""},
        {"name": "申购状态", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_financial_fund_daily_em"},
    ]
