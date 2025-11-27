"""
货币型基金排行-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_money_rank_em_provider import FundMoneyRankEmProvider


class FundMoneyRankEmService(SimpleService):
    """货币型基金排行-东财服务"""
    
    collection_name = "fund_money_rank_em"
    provider_class = FundMoneyRankEmProvider
