"""
基金历史行情-新浪数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundHistSinaProvider(SimpleProvider):
    """基金历史行情-新浪数据提供者"""
    
    collection_name = "fund_hist_sina"
    display_name = "基金历史行情-新浪"
    akshare_func = "fund_hist_sina"
    unique_keys = ["更新时间"]

    field_info = [
        {"name": "date", "type": "string", "description": ""},
        {"name": "open", "type": "float", "description": ""},
        {"name": "high", "type": "float", "description": ""},
        {"name": "low", "type": "float", "description": ""},
        {"name": "close", "type": "float", "description": ""},
        {"name": "volume", "type": "int", "description": "注意单位: 手"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_hist_sina"},
    ]
