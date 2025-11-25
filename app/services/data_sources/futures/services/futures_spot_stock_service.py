"""现货与股票服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_spot_stock_provider import FuturesSpotStockProvider

class FuturesSpotStockService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_spot_stock", FuturesSpotStockProvider())
