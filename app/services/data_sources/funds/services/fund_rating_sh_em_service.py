"""
基金评级-上海证券-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_rating_sh_em_provider import FundRatingShEmProvider


class FundRatingShEmService(SimpleService):
    """基金评级-上海证券-东财服务"""
    
    collection_name = "fund_rating_sh_em"
    provider_class = FundRatingShEmProvider
