"""
香港基金排行-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_hk_rank_em_provider import FundHkRankEmProvider


class FundHkRankEmService(SimpleService):
    """香港基金排行-东财服务"""
    
    collection_name = "fund_hk_rank_em"
    provider_class = FundHkRankEmProvider
