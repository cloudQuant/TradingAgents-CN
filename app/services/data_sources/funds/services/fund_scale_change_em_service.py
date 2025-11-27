"""
基金规模变动-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_scale_change_em_provider import FundScaleChangeEmProvider


class FundScaleChangeEmService(SimpleService):
    """基金规模变动-东财服务"""
    
    collection_name = "fund_scale_change_em"
    provider_class = FundScaleChangeEmProvider
