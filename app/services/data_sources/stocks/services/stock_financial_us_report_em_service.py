"""
美股财务报表服务

东方财富-美股-财务分析-三大报表
接口: stock_financial_us_report_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_financial_us_report_em_provider import StockFinancialUsReportEmProvider


class StockFinancialUsReportEmService(BaseService):
    """美股财务报表服务"""
    
    collection_name = "stock_financial_us_report_em"
    provider_class = StockFinancialUsReportEmProvider
    
    # 时间字段名
    time_field = "更新时间"
