"""
基金盈利概率-雪球服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_individual_profit_probability_xq_provider import FundIndividualProfitProbabilityXqProvider


class FundIndividualProfitProbabilityXqService(SimpleService):
    """基金盈利概率-雪球服务"""
    
    collection_name = "fund_individual_profit_probability_xq"
    provider_class = FundIndividualProfitProbabilityXqProvider
