"""
基金持仓明细-雪球服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_individual_detail_hold_xq_provider import FundIndividualDetailHoldXqProvider


class FundIndividualDetailHoldXqService(SimpleService):
    """基金持仓明细-雪球服务"""
    
    collection_name = "fund_individual_detail_hold_xq"
    provider_class = FundIndividualDetailHoldXqProvider
