"""货币报价历史数据服务"""
from app.services.data_sources.base_service import SimpleService


class CurrencyHistoryService(SimpleService):
    """货币报价历史数据服务"""
    collection_name = "currency_history"
