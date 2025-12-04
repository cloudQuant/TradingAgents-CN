"""
港股财务报表数据提供者

东方财富-港股-财务报表-三大报表
接口: stock_financial_hk_report_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockFinancialHkReportEmProvider(BaseProvider):
    """港股财务报表数据提供者"""
    
    # 必填属性
    collection_name = "stock_financial_hk_report_em"
    display_name = "港股财务报表"
    akshare_func = "stock_financial_hk_report_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-港股-财务报表-三大报表"
    collection_route = "/stocks/collections/stock_financial_hk_report_em"
    collection_category = "财务数据"

    # 参数映射
    param_mapping = {
        "stock": "stock",
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "indicator": "indicator"
    }
    
    # 必填参数
    required_params = ['stock', 'symbol', 'indicator']

    # 字段信息
    field_info = [
        {"name": "SECUCODE", "type": "object", "description": "-"},
        {"name": "SECURITY_CODE", "type": "object", "description": "-"},
        {"name": "SECURITY_NAME_ABBR", "type": "object", "description": "-"},
        {"name": "ORG_CODE", "type": "object", "description": "-"},
        {"name": "REPORT_DATE", "type": "object", "description": "-"},
        {"name": "DATE_TYPE_CODE", "type": "object", "description": "-"},
        {"name": "FISCAL_YEAR", "type": "object", "description": "-"},
        {"name": "STD_ITEM_CODE", "type": "object", "description": "-"},
        {"name": "STD_ITEM_NAME", "type": "object", "description": "-"},
        {"name": "AMOUNT", "type": "float64", "description": "-"},
        {"name": "STD_REPORT_DATE", "type": "object", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
