"""
货币型基金实时行情-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_money_fund_daily_em_provider import FundMoneyFundDailyEmProvider


class FundMoneyFundDailyEmService(SimpleService):
    """货币型基金实时行情-东财服务"""
    
    collection_name = "fund_money_fund_daily_em"
    provider_class = FundMoneyFundDailyEmProvider
