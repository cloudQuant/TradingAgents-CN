"""货币报价最新数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.currencies.providers.currency_latest_provider import (
    CurrencyLatestProvider,
)


class CurrencyLatestService(SimpleService):
    """货币报价最新数据服务"""
    collection_name = "currency_latest"
    provider_class = CurrencyLatestProvider
