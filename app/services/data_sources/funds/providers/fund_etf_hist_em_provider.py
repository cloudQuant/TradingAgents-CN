"""
ETF历史行情-东财数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundEtfHistEmProvider(SimpleProvider):
    
    """ETF历史行情-东财数据提供者"""

    collection_description = "东方财富网-ETF 历史行情数据，支持按代码、周期（日/周/月）、复权方式查询历史K线数据"
    collection_route = "/funds/collections/fund_etf_hist_em"
    collection_order = 12

    collection_name = "fund_etf_hist_em"
    display_name = "ETF基金历史行情-东财"
    akshare_func = "fund_etf_hist_em"
    unique_keys = ["日期"]

    field_info = [
        {"name": "日期", "type": "string", "description": ""},
        {"name": "开盘", "type": "float", "description": ""},
        {"name": "收盘", "type": "float", "description": ""},
        {"name": "最高", "type": "float", "description": ""},
        {"name": "最低", "type": "float", "description": ""},
        {"name": "成交量", "type": "int", "description": ""},
        {"name": "成交额", "type": "float", "description": ""},
        {"name": "振幅", "type": "float", "description": ""},
        {"name": "涨跌幅", "type": "float", "description": ""},
        {"name": "涨跌额", "type": "float", "description": ""},
        {"name": "换手率", "type": "float", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_etf_hist_em"},
    ]
