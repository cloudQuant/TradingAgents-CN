"""
基金分红公告-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_announcement_dividend_em_provider import FundAnnouncementDividendEmProvider


class FundAnnouncementDividendEmService(SimpleService):
    """基金分红公告-东财服务"""
    
    collection_name = "fund_announcement_dividend_em"
    provider_class = FundAnnouncementDividendEmProvider
