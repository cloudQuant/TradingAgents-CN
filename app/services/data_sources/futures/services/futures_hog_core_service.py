"""生猪核心数据服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_hog_core_provider import FuturesHogCoreProvider

class FuturesHogCoreService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_hog_core", FuturesHogCoreProvider())
