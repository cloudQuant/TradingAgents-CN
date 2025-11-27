"""
分级基金历史数据-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_graded_fund_info_em_provider import FundGradedFundInfoEmProvider


class FundGradedFundInfoEmService(SimpleService):
    """分级基金历史数据-东财服务"""
    
    collection_name = "fund_graded_fund_info_em"
    provider_class = FundGradedFundInfoEmProvider
