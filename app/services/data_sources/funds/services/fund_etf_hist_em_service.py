"""
ETF历史行情-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_etf_hist_em_provider import FundEtfHistEmProvider


class FundEtfHistEmService(SimpleService):
    """ETF历史行情-东财服务"""
    
    collection_name = "fund_etf_hist_em"
    provider_class = FundEtfHistEmProvider
