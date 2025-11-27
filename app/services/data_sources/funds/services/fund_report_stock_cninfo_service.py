"""
基金报告持股-巨潮服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_report_stock_cninfo_provider import FundReportStockCninfoProvider


class FundReportStockCninfoService(SimpleService):
    """基金报告持股-巨潮服务"""
    
    collection_name = "fund_report_stock_cninfo"
    provider_class = FundReportStockCninfoProvider
