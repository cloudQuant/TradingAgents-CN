"""
新发基金-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_new_found_em_provider import FundNewFoundEmProvider


class FundNewFoundEmService(SimpleService):
    """新发基金-东财服务"""
    
    collection_name = "fund_new_found_em"
    provider_class = FundNewFoundEmProvider
