"""
场内交易基金实时数据-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_etf_fund_daily_em_provider import FundEtfFundDailyEmProvider


class FundEtfFundDailyEmService(SimpleService):
    """场内交易基金实时数据-东财服务"""
    
    collection_name = "fund_etf_fund_daily_em"
    provider_class = FundEtfFundDailyEmProvider
