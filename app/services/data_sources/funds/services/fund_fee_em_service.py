"""
基金费率-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_fee_em_provider import FundFeeEmProvider


class FundFeeEmService(SimpleService):
    """基金费率-东财服务"""
    
    collection_name = "fund_fee_em"
    provider_class = FundFeeEmProvider
