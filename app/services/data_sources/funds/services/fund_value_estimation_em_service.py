"""
基金净值估算-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_value_estimation_em_provider import FundValueEstimationEmProvider


class FundValueEstimationEmService(SimpleService):
    """基金净值估算-东财服务"""
    
    collection_name = "fund_value_estimation_em"
    provider_class = FundValueEstimationEmProvider
