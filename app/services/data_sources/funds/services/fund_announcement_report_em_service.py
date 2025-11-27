"""
基金报告公告-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_announcement_report_em_provider import FundAnnouncementReportEmProvider


class FundAnnouncementReportEmService(SimpleService):
    """基金报告公告-东财服务"""
    
    collection_name = "fund_announcement_report_em"
    provider_class = FundAnnouncementReportEmProvider
