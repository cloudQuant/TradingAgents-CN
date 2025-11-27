"""
基金概况-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_overview_em_provider import FundOverviewEmProvider


class FundOverviewEmService(SimpleService):
    """基金概况-东财服务"""
    
    collection_name = "fund_overview_em"
    provider_class = FundOverviewEmProvider
