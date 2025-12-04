"""
港股财务报表服务

东方财富-港股-财务报表-三大报表
接口: stock_financial_hk_report_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_financial_hk_report_em_provider import StockFinancialHkReportEmProvider


class StockFinancialHkReportEmService(BaseService):
    """港股财务报表服务"""
    
    collection_name = "stock_financial_hk_report_em"
    provider_class = StockFinancialHkReportEmProvider
    
    # 时间字段名
    time_field = "更新时间"
