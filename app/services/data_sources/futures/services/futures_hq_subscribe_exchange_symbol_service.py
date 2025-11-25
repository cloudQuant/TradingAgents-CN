"""外盘品种代码表服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_hq_subscribe_exchange_symbol_provider import FuturesHqSubscribeExchangeSymbolProvider

class FuturesHqSubscribeExchangeSymbolService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_hq_subscribe_exchange_symbol", FuturesHqSubscribeExchangeSymbolProvider())
