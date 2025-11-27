"""
基金分红排行-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_fh_rank_em_provider import FundFhRankEmProvider


class FundFhRankEmService(SimpleService):
    """基金分红排行-东财服务"""
    
    collection_name = "fund_fh_rank_em"
    provider_class = FundFhRankEmProvider
