"""
基金管理规模-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_aum_em_provider import FundAumEmProvider


class FundAumEmService(SimpleService):
    """基金管理规模-东财服务"""
    
    collection_name = "fund_aum_em"
    provider_class = FundAumEmProvider
