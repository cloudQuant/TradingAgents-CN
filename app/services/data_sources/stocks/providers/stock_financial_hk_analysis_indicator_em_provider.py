"""
港股财务指标数据提供者

东方财富-港股-财务分析-主要指标
接口: stock_financial_hk_analysis_indicator_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockFinancialHkAnalysisIndicatorEmProvider(BaseProvider):
    """港股财务指标数据提供者"""
    
    # 必填属性
    collection_name = "stock_financial_hk_analysis_indicator_em"
    display_name = "港股财务指标"
    akshare_func = "stock_financial_hk_analysis_indicator_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-港股-财务分析-主要指标"
    collection_route = "/stocks/collections/stock_financial_hk_analysis_indicator_em"
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
        {"name": "SECUCODE", "type": "object", "description": "股票代码(带HK后缀)"},
        {"name": "SECURITY_CODE", "type": "object", "description": "股票代码(不带HK后缀)"},
        {"name": "ORG_CODE", "type": "object", "description": "ORG_CODE"},
        {"name": "REPORT_DATE", "type": "object", "description": "报告日期"},
        {"name": "DATE_TYPE_CODE", "type": "object", "description": "报告日期类型"},
        {"name": "PER_NETCASH_OPERATE", "type": "float64", "description": "每股经营现金流(元)"},
        {"name": "PER_OI", "type": "float64", "description": "每股营业收入(元)"},
        {"name": "BPS", "type": "float64", "description": "每股净资产(元)"},
        {"name": "BASIC_EPS", "type": "float64", "description": "基本每股收益(元)"},
        {"name": "DILUTED_EPS", "type": "float64", "description": "稀释每股收益(元)"},
        {"name": "OPERATE_INCOME", "type": "int64", "description": "营业总收入(元)"},
        {"name": "OPERATE_INCOME_YOY", "type": "float64", "description": "营业总收入同比增长(%)"},
        {"name": "GROSS_PROFIT", "type": "int64", "description": "毛利润(元)"},
        {"name": "GROSS_PROFIT_YOY", "type": "float64", "description": "毛利润同比增长(%)"},
        {"name": "HOLDER_PROFIT", "type": "int64", "description": "归母净利润(元)"},
        {"name": "HOLDER_PROFIT_YOY", "type": "float64", "description": "归母净利润同比增长(%)"},
        {"name": "GROSS_PROFIT_RATIO", "type": "float64", "description": "毛利率(%)"},
        {"name": "EPS_TTM", "type": "float64", "description": "TTM每股收益(元)"},
        {"name": "OPERATE_INCOME_QOQ", "type": "float64", "description": "营业总收入滚动环比增长(%)"},
        {"name": "NET_PROFIT_RATIO", "type": "float64", "description": "净利率(%)"},
        {"name": "ROE_AVG", "type": "float64", "description": "平均净资产收益率(%)"},
        {"name": "GROSS_PROFIT_QOQ", "type": "float64", "description": "毛利润滚动环比增长(%)"},
        {"name": "ROA", "type": "float64", "description": "总资产净利率(%)"},
        {"name": "HOLDER_PROFIT_QOQ", "type": "float64", "description": "归母净利润滚动环比增长(%)"},
        {"name": "ROE_YEARLY", "type": "float64", "description": "年化净资产收益率(%)"},
        {"name": "ROIC_YEARLY", "type": "float64", "description": "年化投资回报率(%)"},
        {"name": "TAX_EBT", "type": "float64", "description": "所得税/利润总额(%)"},
        {"name": "OCF_SALES", "type": "float64", "description": "经营现金流/营业收入(%)"},
        {"name": "DEBT_ASSET_RATIO", "type": "float64", "description": "资产负债率(%)"},
        {"name": "CURRENT_RATIO", "type": "float64", "description": "流动比率(倍)"},
        {"name": "CURRENTDEBT_DEBT", "type": "float64", "description": "流动负债/总负债(%)"},
        {"name": "START_DATE", "type": "object", "description": "START_DATE"},
        {"name": "FISCAL_YEAR", "type": "object", "description": "年结日"},
        {"name": "CURRENCY", "type": "object", "description": "CURRENCY"},
        {"name": "IS_CNY_CODE", "type": "int64", "description": "IS_CNY_CODE"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
