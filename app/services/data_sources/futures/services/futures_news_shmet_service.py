"""期货资讯服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_news_shmet_provider import FuturesNewsShmetProvider

class FuturesNewsShmetService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_news_shmet", FuturesNewsShmetProvider())
