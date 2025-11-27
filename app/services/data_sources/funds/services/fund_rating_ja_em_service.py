"""
基金评级-济安金信-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_rating_ja_em_provider import FundRatingJaEmProvider


class FundRatingJaEmService(SimpleService):
    """基金评级-济安金信-东财服务"""
    
    collection_name = "fund_rating_ja_em"
    provider_class = FundRatingJaEmProvider
