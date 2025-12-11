"""货币对价格转换服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.currencies.providers.currency_convert_provider import (
    CurrencyConvertProvider,
)


class CurrencyConvertService(SimpleService):
    """货币对价格转换服务"""
    collection_name = "currency_convert"
    provider_class = CurrencyConvertProvider
