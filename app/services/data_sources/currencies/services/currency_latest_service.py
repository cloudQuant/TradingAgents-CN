"""货币报价最新数据服务"""
from app.services.data_sources.base_service import SimpleService


class CurrencyLatestService(SimpleService):
    """货币报价最新数据服务"""
    collection_name = "currency_latest"
