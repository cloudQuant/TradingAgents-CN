"""东财期权分时行情数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_minute_em_provider import OptionMinuteEmProvider


class OptionMinuteEmService(SimpleService):
    """东财期权分时行情数据服务"""
    collection_name = "option_minute_em"
    provider_class = OptionMinuteEmProvider
