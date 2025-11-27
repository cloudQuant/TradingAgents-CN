"""
指数型基金基本信息-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundInfoIndexEmProvider(SimpleProvider):
    """指数型基金基本信息-东财数据提供者"""
    
    collection_name = "fund_info_index_em"
    display_name = "指数型基金基本信息-东财"
    akshare_func = "fund_info_index_em"
    unique_keys = ["基金代码", "日期"]

    field_info = [
        {"name": "基金代码", "type": "string", "description": ""},
        {"name": "基金名称", "type": "string", "description": ""},
        {"name": "单位净值", "type": "float", "description": ""},
        {"name": "日期", "type": "string", "description": ""},
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
        {"name": "手续费", "type": "float", "description": "注意单位: %"},
        {"name": "起购金额", "type": "string", "description": ""},
        {"name": "跟踪标的", "type": "string", "description": ""},
        {"name": "跟踪方式", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_info_index_em"},
    ]
