"""金融期权股票期权分时行情数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionFinanceMinuteSinaService(SimpleService):
    """金融期权股票期权分时行情数据服务"""
    collection_name = "option_finance_minute_sina"
