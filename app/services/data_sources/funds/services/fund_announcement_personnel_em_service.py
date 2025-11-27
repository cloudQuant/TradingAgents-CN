"""
基金人事公告-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_announcement_personnel_em_provider import FundAnnouncementPersonnelEmProvider


class FundAnnouncementPersonnelEmService(SimpleService):
    """基金人事公告-东财服务"""
    
    collection_name = "fund_announcement_personnel_em"
    provider_class = FundAnnouncementPersonnelEmProvider
