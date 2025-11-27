"""
场内基金排行-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_exchange_rank_em_provider import FundExchangeRankEmProvider


class FundExchangeRankEmService(SimpleService):
    """场内基金排行-东财服务"""
    
    collection_name = "fund_exchange_rank_em"
    provider_class = FundExchangeRankEmProvider
