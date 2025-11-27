"""
ETF实时行情-同花顺服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_etf_spot_ths_provider import FundEtfSpotThsProvider


class FundEtfSpotThsService(SimpleService):
    """ETF实时行情-同花顺服务"""
    
    collection_name = "fund_etf_spot_ths"
    provider_class = FundEtfSpotThsProvider
