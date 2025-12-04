"""
美股财务指标数据提供者

东方财富-美股-财务分析-主要指标
接口: stock_financial_us_analysis_indicator_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockFinancialUsAnalysisIndicatorEmProvider(BaseProvider):
    """美股财务指标数据提供者"""
    
    # 必填属性
    collection_name = "stock_financial_us_analysis_indicator_em"
    display_name = "美股财务指标"
    akshare_func = "stock_financial_us_analysis_indicator_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-美股-财务分析-主要指标"
    collection_route = "/stocks/collections/stock_financial_us_analysis_indicator_em"
    collection_category = "财务数据"

    # 参数映射
    param_mapping = {
        "symbol": "symbol",
        "code": "symbol",
        "stock_code": "symbol",
        "indicator": "indicator"
    }
    
    # 必填参数
    required_params = ['symbol', 'indicator']

    # 字段信息
    field_info = [
        {"name": "SECUCODE", "type": "object", "description": "-"},
        {"name": "SECURITY_CODE", "type": "object", "description": "-"},
        {"name": "SECURITY_NAME_ABBR", "type": "object", "description": "-"},
        {"name": "ORG_CODE", "type": "object", "description": "-"},
        {"name": "SECURITY_INNER_CODE", "type": "object", "description": "-"},
        {"name": "ACCOUNTING_STANDARDS", "type": "object", "description": "-"},
        {"name": "NOTICE_DATE", "type": "object", "description": "-"},
        {"name": "START_DATE", "type": "object", "description": "-"},
        {"name": "REPORT_DATE", "type": "object", "description": "-"},
        {"name": "FINANCIAL_DATE", "type": "object", "description": "-"},
        {"name": "STD_REPORT_DATE", "type": "object", "description": "-"},
        {"name": "CURRENCY", "type": "object", "description": "-"},
        {"name": "DATE_TYPE", "type": "object", "description": "-"},
        {"name": "DATE_TYPE_CODE", "type": "object", "description": "-"},
        {"name": "REPORT_TYPE", "type": "object", "description": "-"},
        {"name": "REPORT_DATA_TYPE", "type": "object", "description": "-"},
        {"name": "ORGTYPE", "type": "object", "description": "-"},
        {"name": "OPERATE_INCOME", "type": "float64", "description": "-"},
        {"name": "OPERATE_INCOME_YOY", "type": "float64", "description": "-"},
        {"name": "GROSS_PROFIT", "type": "float64", "description": "-"},
        {"name": "GROSS_PROFIT_YOY", "type": "float64", "description": "-"},
        {"name": "PARENT_HOLDER_NETPROFIT", "type": "int64", "description": "-"},
        {"name": "PARENT_HOLDER_NETPROFIT_YOY", "type": "float64", "description": "-"},
        {"name": "BASIC_EPS", "type": "float64", "description": "-"},
        {"name": "DILUTED_EPS", "type": "float64", "description": "-"},
        {"name": "GROSS_PROFIT_RATIO", "type": "float64", "description": "-"},
        {"name": "NET_PROFIT_RATIO", "type": "float64", "description": "-"},
        {"name": "ACCOUNTS_RECE_TR", "type": "float64", "description": "-"},
        {"name": "INVENTORY_TR", "type": "float64", "description": "-"},
        {"name": "TOTAL_ASSETS_TR", "type": "float64", "description": "-"},
        {"name": "ACCOUNTS_RECE_TDAYS", "type": "float64", "description": "-"},
        {"name": "INVENTORY_TDAYS", "type": "float64", "description": "-"},
        {"name": "TOTAL_ASSETS_TDAYS", "type": "float64", "description": "-"},
        {"name": "ROE_AVG", "type": "float64", "description": "-"},
        {"name": "ROA", "type": "float64", "description": "-"},
        {"name": "CURRENT_RATIO", "type": "float64", "description": "-"},
        {"name": "SPEED_RATIO", "type": "float64", "description": "-"},
        {"name": "OCF_LIQDEBT", "type": "float64", "description": "-"},
        {"name": "DEBT_ASSET_RATIO", "type": "float64", "description": "-"},
        {"name": "EQUITY_RATIO", "type": "float64", "description": "-"},
        {"name": "BASIC_EPS_YOY", "type": "float64", "description": "-"},
        {"name": "GROSS_PROFIT_RATIO_YOY", "type": "float64", "description": "-"},
        {"name": "NET_PROFIT_RATIO_YOY", "type": "float64", "description": "-"},
        {"name": "ROE_AVG_YOY", "type": "float64", "description": "-"},
        {"name": "ROA_YOY", "type": "float64", "description": "-"},
        {"name": "DEBT_ASSET_RATIO_YOY", "type": "float64", "description": "-"},
        {"name": "CURRENT_RATIO_YOY", "type": "float64", "description": "-"},
        {"name": "SPEED_RATIO_YOY", "type": "float64", "description": "-"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
