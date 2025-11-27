"""
基金实时行情-新浪服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_spot_sina_provider import FundSpotSinaProvider


class FundSpotSinaService(SimpleService):
    """基金实时行情-新浪服务"""
    
    collection_name = "fund_spot_sina"
    provider_class = FundSpotSinaProvider
