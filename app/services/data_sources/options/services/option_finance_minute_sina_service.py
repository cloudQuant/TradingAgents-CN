"""金融期权股票期权分时行情数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_finance_minute_sina_provider import OptionFinanceMinuteSinaProvider


class OptionFinanceMinuteSinaService(SimpleService):
    """金融期权股票期权分时行情数据服务"""
    collection_name = "option_finance_minute_sina"
    provider_class = OptionFinanceMinuteSinaProvider
