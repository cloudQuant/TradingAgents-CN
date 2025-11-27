"""
基金详细信息-雪球服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_individual_detail_info_xq_provider import FundIndividualDetailInfoXqProvider


class FundIndividualDetailInfoXqService(SimpleService):
    """基金详细信息-雪球服务"""
    
    collection_name = "fund_individual_detail_info_xq"
    provider_class = FundIndividualDetailInfoXqProvider
