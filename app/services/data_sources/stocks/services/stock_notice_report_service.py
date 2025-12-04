"""
沪深京 A 股公告服务

东方财富网-数据中心-公告大全-沪深京 A 股公告
接口: stock_notice_report
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_notice_report_provider import StockNoticeReportProvider


class StockNoticeReportService(BaseService):
    """沪深京 A 股公告服务"""
    
    collection_name = "stock_notice_report"
    provider_class = StockNoticeReportProvider
    
    # 时间字段名
    time_field = "更新时间"
