"""
基金累计分红-新浪数据提供者（重构版：继承SimpleProvider）
"""
from app.services.data_sources.base_provider import SimpleProvider


class FundEtfDividendSinaProvider(SimpleProvider):
    """基金累计分红-新浪数据提供者"""
    
    collection_name = "fund_etf_dividend_sina"
    display_name = "基金累计分红-新浪"
    akshare_func = "fund_etf_dividend_sina"
    unique_keys = ["日期"]

    field_info = [
        {"name": "日期", "type": "string", "description": "除权除息日"},
        {"name": "累计分红", "type": "float", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_etf_dividend_sina"},
    ]
