"""货币基础信息查询服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.currencies.providers.currency_currencies_provider import (
    CurrencyCurrenciesProvider,
)


class CurrencyCurrenciesService(SimpleService):
    """货币基础信息查询服务"""
    collection_name = "currency_currencies"
    provider_class = CurrencyCurrenciesProvider
