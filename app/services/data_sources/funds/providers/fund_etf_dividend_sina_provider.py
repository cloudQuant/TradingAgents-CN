"""
基金累计分红-新浪数据提供者（重构版：继承BaseProvider）
"""
from app.services.data_sources.base_provider import BaseProvider


class FundEtfDividendSinaProvider(BaseProvider):
    
    """基金累计分红-新浪数据提供者"""

    collection_description = "新浪财经-ETF基金累计分红数据，包含除权除息日、累计分红金额"
    collection_route = "/funds/collections/fund_etf_dividend_sina"
    collection_order = 26

    collection_name = "fund_etf_dividend_sina"
    display_name = "基金累计分红-新浪"
    akshare_func = "fund_etf_dividend_sina"
    unique_keys = ["代码", "日期", "基金简称"]
    
    # 参数映射：支持 fund_code/code/symbol
    param_mapping = {
        "fund_code": "symbol",
        "code": "symbol",
        "symbol": "symbol",
    }
    required_params = ["symbol"]
    
    # 自动添加代码字段到数据中
    add_param_columns = {
        "symbol": "代码",  # 将 symbol 参数值写入 "代码" 列
    }

    field_info = [
        {"name": "代码", "type": "string", "description": "基金代码（如 sh510050）"},
        {"name": "日期", "type": "string", "description": "除权除息日"},
        {"name": "累计分红", "type": "float", "description": ""},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "更新人", "type": "string", "description": "数据更新人"},
        {"name": "创建时间", "type": "datetime", "description": "数据创建时间"},
        {"name": "创建人", "type": "string", "description": "数据创建人"},
        {"name": "来源", "type": "string", "description": "来源接口: fund_etf_dividend_sina"},
    ]
    
