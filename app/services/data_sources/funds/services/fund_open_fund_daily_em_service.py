"""
开放式基金实时行情-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_open_fund_daily_em_provider import FundOpenFundDailyEmProvider


class FundOpenFundDailyEmService(SimpleService):
    """开放式基金实时行情-东财服务"""
    
    collection_name = "fund_open_fund_daily_em"
    provider_class = FundOpenFundDailyEmProvider
