"""
开放式基金实时行情-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundOpenFundDailyEmProvider(SimpleProvider):
    """开放式基金实时行情-东财数据提供者"""
    
    collection_name = "fund_open_fund_daily_em"
    display_name = "开放式基金实时行情-东财"
    akshare_func = "fund_open_fund_daily_em"
    unique_keys = ["基金代码", "更新时间"]

    field_info = [
        {"name": "基金代码", "type": "string", "description": ""},
        {"name": "基金简称", "type": "string", "description": ""},
        {"name": "单位净值", "type": "float", "description": "随时间变动"},
        {"name": "累计净值", "type": "float", "description": "随时间变动"},
        {"name": "前交易日-单位净值", "type": "float", "description": "随时间变动"},
        {"name": "前交易日-累计净值", "type": "float", "description": "随时间变动"},
        {"name": "日增长值", "type": "float", "description": ""},
        {"name": "日增长率", "type": "float", "description": ""},
        {"name": "申购状态", "type": "string", "description": ""},
        {"name": "赎回状态", "type": "string", "description": ""},
        {"name": "手续费", "type": "string", "description": "注意单位: %"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_open_fund_daily_em"},
    ]
