"""
基金业绩表现-雪球服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_individual_achievement_xq_provider import FundIndividualAchievementXqProvider


class FundIndividualAchievementXqService(SimpleService):
    """基金业绩表现-雪球服务"""
    
    collection_name = "fund_individual_achievement_xq"
    provider_class = FundIndividualAchievementXqProvider
