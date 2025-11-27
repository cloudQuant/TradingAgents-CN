"""
ETF实时行情-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_etf_spot_em_provider import FundEtfSpotEmProvider


class FundEtfSpotEmService(SimpleService):
    """ETF实时行情-东财服务"""
    
    collection_name = "fund_etf_spot_em"
    provider_class = FundEtfSpotEmProvider
