"""
ETF分时行情-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundEtfHistMinEmProvider(SimpleProvider):
    
    """ETF分时行情-东财数据提供者"""

    collection_description = "东方财富网-ETF 分时行情数据，支持按代码、时间周期、复权方式查询近期分钟级行情"
    collection_route = "/funds/collections/fund_etf_hist_min_em"
    collection_order = 10

    collection_name = "fund_etf_hist_min_em"
    display_name = "ETF基金分时行情-东财"
    akshare_func = "fund_etf_hist_min_em"
    unique_keys = ["时间"]

    field_info = [
        {"name": "时间", "type": "string", "description": ""},
        {"name": "开盘", "type": "float", "description": ""},
        {"name": "收盘", "type": "float", "description": ""},
        {"name": "最高", "type": "float", "description": ""},
        {"name": "最低", "type": "float", "description": ""},
        {"name": "成交量", "type": "float", "description": ""},
        {"name": "成交额", "type": "float", "description": ""},
        {"name": "均价", "type": "float", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_etf_hist_min_em"},
    ]
