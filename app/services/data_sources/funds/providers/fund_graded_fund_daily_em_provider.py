"""
分级基金实时数据-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundGradedFundDailyEmProvider(SimpleProvider):
    """分级基金实时数据-东财数据提供者"""
    
    collection_name = "fund_graded_fund_daily_em"
    display_name = "分级基金实时数据-东财"
    akshare_func = "fund_graded_fund_daily_em"
    unique_keys = ["基金代码", "更新时间"]

    field_info = [
        {"name": "基金代码", "type": "string", "description": ""},
        {"name": "基金简称", "type": "string", "description": ""},
        {"name": "单位净值", "type": "float", "description": ""},
        {"name": "累计净值", "type": "float", "description": ""},
        {"name": "前交易日-单位净值", "type": "float", "description": ""},
        {"name": "前交易日-累计净值", "type": "float", "description": ""},
        {"name": "日增长值", "type": "float", "description": ""},
        {"name": "日增长率", "type": "float", "description": "注意单位: %"},
        {"name": "市价", "type": "string", "description": ""},
        {"name": "折价率", "type": "string", "description": ""},
        {"name": "手续费", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_graded_fund_daily_em"},
    ]
