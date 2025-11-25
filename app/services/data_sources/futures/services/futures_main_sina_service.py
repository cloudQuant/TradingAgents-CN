"""期货连续合约服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_main_sina_provider import FuturesMainSinaProvider

class FuturesMainSinaService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_main_sina", FuturesMainSinaProvider())
