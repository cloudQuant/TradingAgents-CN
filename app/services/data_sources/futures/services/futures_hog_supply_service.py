"""生猪供应数据服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_hog_supply_provider import FuturesHogSupplyProvider

class FuturesHogSupplyService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_hog_supply", FuturesHogSupplyProvider())
