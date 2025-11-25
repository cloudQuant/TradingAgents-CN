"""生猪成本数据服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_hog_cost_provider import FuturesHogCostProvider

class FuturesHogCostService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_hog_cost", FuturesHogCostProvider())
