"""COMEX库存数据服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_comex_inventory_provider import FuturesComexInventoryProvider

class FuturesComexInventoryService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_comex_inventory", FuturesComexInventoryProvider())
