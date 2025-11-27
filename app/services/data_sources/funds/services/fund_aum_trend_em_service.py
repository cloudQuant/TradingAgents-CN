"""
基金规模趋势-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_aum_trend_em_provider import FundAumTrendEmProvider


class FundAumTrendEmService(SimpleService):
    """基金规模趋势-东财服务"""
    
    collection_name = "fund_aum_trend_em"
    provider_class = FundAumTrendEmProvider
