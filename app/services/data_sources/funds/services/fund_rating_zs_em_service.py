"""
基金评级-招商证券-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_rating_zs_em_provider import FundRatingZsEmProvider


class FundRatingZsEmService(SimpleService):
    """基金评级-招商证券-东财服务"""
    
    collection_name = "fund_rating_zs_em"
    provider_class = FundRatingZsEmProvider
