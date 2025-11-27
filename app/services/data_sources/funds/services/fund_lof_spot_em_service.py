"""
LOF实时行情-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_lof_spot_em_provider import FundLofSpotEmProvider


class FundLofSpotEmService(SimpleService):
    """LOF实时行情-东财服务"""
    
    collection_name = "fund_lof_spot_em"
    provider_class = FundLofSpotEmProvider
