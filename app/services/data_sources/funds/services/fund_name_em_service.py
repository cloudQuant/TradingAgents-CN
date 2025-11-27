"""
基金基本信息-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_name_em_provider import FundNameEmProvider


class FundNameEmService(SimpleService):
    """基金基本信息-东财服务"""
    
    collection_name = "fund_name_em"
    provider_class = FundNameEmProvider
