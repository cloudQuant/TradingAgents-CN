"""
基金规模趋势-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundAumTrendEmProvider(SimpleProvider):
    """基金规模趋势-东财数据提供者"""
    
    collection_name = "fund_aum_trend_em"
    display_name = "基金规模趋势-东财"
    akshare_func = "fund_aum_trend_em"
    unique_keys = ["更新时间"]

    field_info = [
        {"name": "date", "type": "string", "description": ""},
        {"name": "value", "type": "float", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_aum_trend_em"},
    ]
