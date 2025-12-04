"""外盘-品种代码表服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesHqSubscribeExchangeSymbolService(SimpleService):
    """外盘-品种代码表服务"""
    collection_name = "futures_hq_subscribe_exchange_symbol"
