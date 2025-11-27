"""
香港基金历史数据-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundHkHistEmProvider(SimpleProvider):
    """香港基金历史数据-东财数据提供者"""
    
    collection_name = "fund_hk_hist_em"
    display_name = "香港基金历史数据-东财"
    akshare_func = "fund_hk_hist_em"
    unique_keys = ["净值日期"]

    field_info = [
        {"name": "净值日期", "type": "string", "description": ""},
        {"name": "单位净值", "type": "float", "description": ""},
        {"name": "日增长值", "type": "float", "description": ""},
        {"name": "日增长率", "type": "float", "description": "注意单位: %"},
        {"name": "单位", "type": "string", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_hk_hist_em"},
    ]
