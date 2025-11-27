"""
LOF分时行情-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_lof_hist_min_em_provider import FundLofHistMinEmProvider


class FundLofHistMinEmService(SimpleService):
    """LOF分时行情-东财服务"""
    
    collection_name = "fund_lof_hist_min_em"
    provider_class = FundLofHistMinEmProvider
