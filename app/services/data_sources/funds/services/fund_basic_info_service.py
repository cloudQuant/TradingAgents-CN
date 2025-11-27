"""
基金基本信息-雪球服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_basic_info_provider import FundBasicInfoProvider


class FundBasicInfoService(SimpleService):
    """基金基本信息-雪球服务"""
    
    collection_name = "fund_basic_info"
    provider_class = FundBasicInfoProvider
