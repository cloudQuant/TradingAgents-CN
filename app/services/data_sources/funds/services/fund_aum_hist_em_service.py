"""
基金规模历史-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_aum_hist_em_provider import FundAumHistEmProvider


class FundAumHistEmService(SimpleService):
    """基金规模历史-东财服务"""
    
    collection_name = "fund_aum_hist_em"
    provider_class = FundAumHistEmProvider
