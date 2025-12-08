"""外盘-品种代码表服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_hq_subscribe_exchange_symbol_provider import FuturesHqSubscribeExchangeSymbolProvider


class FuturesHqSubscribeExchangeSymbolService(SimpleService):
    """外盘-品种代码表服务"""
    collection_name = "futures_hq_subscribe_exchange_symbol"
    provider_class = FuturesHqSubscribeExchangeSymbolProvider
