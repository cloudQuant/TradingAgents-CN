"""
开放式基金排行-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundOpenFundRankEmProvider(SimpleProvider):
    """开放式基金排行-东财数据提供者"""
    
    collection_name = "fund_open_fund_rank_em"
    display_name = "开放式基金排行-东财"
    akshare_func = "fund_open_fund_rank_em"
    unique_keys = ["基金代码", "日期"]

    field_info = [
        {"name": "序号", "type": "int", "description": ""},
        {"name": "基金代码", "type": "string", "description": ""},
        {"name": "基金简称", "type": "string", "description": ""},
        {"name": "日期", "type": "string", "description": ""},
        {"name": "单位净值", "type": "float", "description": ""},
        {"name": "累计净值", "type": "float", "description": ""},
        {"name": "日增长率", "type": "float", "description": "注意单位: %"},
        {"name": "近1周", "type": "float", "description": "注意单位: %"},
        {"name": "近1月", "type": "float", "description": "注意单位: %"},
        {"name": "近3月", "type": "float", "description": "注意单位: %"},
        {"name": "近6月", "type": "float", "description": "注意单位: %"},
        {"name": "近1年", "type": "float", "description": "注意单位: %"},
        {"name": "近2年", "type": "float", "description": "注意单位: %"},
        {"name": "近3年", "type": "float", "description": "注意单位: %"},
        {"name": "今年来", "type": "float", "description": "注意单位: %"},
        {"name": "成立来", "type": "float", "description": "注意单位: %"},
        {"name": "自定义", "type": "float", "description": "注意单位: %"},
        {"name": "手续费", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_open_fund_rank_em"},
    ]
