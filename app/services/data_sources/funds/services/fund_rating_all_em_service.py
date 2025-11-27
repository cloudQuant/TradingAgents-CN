"""
基金评级汇总-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_rating_all_em_provider import FundRatingAllEmProvider


class FundRatingAllEmService(SimpleService):
    """基金评级汇总-东财服务"""
    
    collection_name = "fund_rating_all_em"
    provider_class = FundRatingAllEmProvider
