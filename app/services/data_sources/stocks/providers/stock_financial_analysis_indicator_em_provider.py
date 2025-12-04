"""
主要指标-东方财富数据提供者

东方财富-A股-财务分析-主要指标
接口: stock_financial_analysis_indicator_em
"""
from app.services.data_sources.base_provider import BaseProvider


class StockFinancialAnalysisIndicatorEmProvider(BaseProvider):
    """主要指标-东方财富数据提供者"""
    
    # 必填属性
    collection_name = "stock_financial_analysis_indicator_em"
    display_name = "主要指标-东方财富"
    akshare_func = "stock_financial_analysis_indicator_em"
    unique_keys = ['代码']
    
    # 可选属性
    collection_description = "东方财富-A股-财务分析-主要指标"
    collection_route = "/stocks/collections/stock_financial_analysis_indicator_em"
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
        {"name": "SECUCODE", "type": "object", "description": "股票代码(带后缀)"},
        {"name": "SECURITY_CODE", "type": "object", "description": "股票代码"},
        {"name": "REPORT_DATE", "type": "object", "description": "报告日期"},
        {"name": "REPORT_TYPE", "type": "object", "description": "报告类型"},
        {"name": "EPSJB", "type": "float64", "description": "基本每股收益(元)"},
        {"name": "EPSKCJB", "type": "float64", "description": "扣非每股收益(元)"},
        {"name": "EPSXS", "type": "float64", "description": "稀释每股收益(元)"},
        {"name": "BPS", "type": "float64", "description": "每股净资产(元)"},
        {"name": "MGZBGJ", "type": "float64", "description": "每股公积金(元)"},
        {"name": "MGWFPLR", "type": "float64", "description": "每股未分配利润(元)"},
        {"name": "MGJYXJJE", "type": "float64", "description": "每股经营现金流(元)"},
        {"name": "TOTALOPERATEREVE", "type": "float64", "description": "营业总收入(元)"},
        {"name": "MLR", "type": "float64", "description": "毛利润(元)"},
        {"name": "PARENTNETPROFIT", "type": "float64", "description": "归属净利润(元)"},
        {"name": "KCFJCXSYJLR", "type": "float64", "description": "扣非净利润(元)"},
        {"name": "TOTALOPERATEREVETZ", "type": "float64", "description": "营业总收入同比增长(%)"},
        {"name": "PARENTNETPROFITTZ", "type": "float64", "description": "归属净利润同比增长(%)"},
        {"name": "KCFJCXSYJLRTZ", "type": "float64", "description": "扣非净利润同比增长(%)"},
        {"name": "YYZSRGDHBZC", "type": "float64", "description": "营业总收入滚动环比增长(%)"},
        {"name": "NETPROFITRPHBZC", "type": "float64", "description": "归属净利润滚动环比增长(%)"},
        {"name": "KFJLRGDHBZC", "type": "float64", "description": "扣非净利润滚动环比增长(%)"},
        {"name": "ROEJQ", "type": "float64", "description": "净资产收益率(加权)(%)"},
        {"name": "ROEKCJQ", "type": "float64", "description": "净资产收益率(扣非/加权)(%)"},
        {"name": "ZZCJLL", "type": "float64", "description": "总资产收益率(加权)(%)"},
        {"name": "XSJLL", "type": "float64", "description": "净利率(%)"},
        {"name": "XSMLL", "type": "float64", "description": "毛利率(%)"},
        {"name": "YSZKYYSR", "type": "float64", "description": "预收账款/营业收入"},
        {"name": "XSJXLYYSR", "type": "float64", "description": "销售净现金流/营业收入"},
        {"name": "JYXJLYYSR", "type": "float64", "description": "经营净现金流/营业收入"},
        {"name": "TAXRATE", "type": "float64", "description": "实际税率(%)"},
        {"name": "LD", "type": "float64", "description": "流动比率"},
        {"name": "SD", "type": "float64", "description": "速动比率"},
        {"name": "XJLLB", "type": "float64", "description": "现金流量比率"},
        {"name": "ZCFZL", "type": "float64", "description": "资产负债率(%)"},
        {"name": "QYCS", "type": "float64", "description": "权益系数"},
        {"name": "CQBL", "type": "float64", "description": "产权比率"},
        {"name": "ZZCZZTS", "type": "float64", "description": "总资产周转天数(天)"},
        {"name": "CHZZTS", "type": "float64", "description": "存货周转天数(天)"},
        {"name": "YSZKZZTS", "type": "float64", "description": "应收账款周转天数(天)"},
        {"name": "TOAZZL", "type": "float64", "description": "总资产周转率(次)"},
        {"name": "CHZZL", "type": "float64", "description": "存货周转率(次)"},
        {"name": "YSZKZZL", "type": "float64", "description": "应收账款周转率(次)"},
        {"name": "...", "type": "...", "description": "..."},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
    ]
