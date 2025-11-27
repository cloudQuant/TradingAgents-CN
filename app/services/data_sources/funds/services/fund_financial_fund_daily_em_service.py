"""
理财型基金实时行情-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_financial_fund_daily_em_provider import FundFinancialFundDailyEmProvider


class FundFinancialFundDailyEmService(SimpleService):
    """理财型基金实时行情-东财服务"""
    
    collection_name = "fund_financial_fund_daily_em"
    provider_class = FundFinancialFundDailyEmProvider
