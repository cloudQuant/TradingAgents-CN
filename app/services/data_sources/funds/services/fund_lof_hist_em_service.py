"""
LOF历史行情-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_lof_hist_em_provider import FundLofHistEmProvider


class FundLofHistEmService(SimpleService):
    """LOF历史行情-东财服务"""
    
    collection_name = "fund_lof_hist_em"
    provider_class = FundLofHistEmProvider
