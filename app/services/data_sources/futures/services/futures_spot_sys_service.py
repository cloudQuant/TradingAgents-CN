"""现期图服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_spot_sys_provider import FuturesSpotSysProvider

class FuturesSpotSysService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_spot_sys", FuturesSpotSysProvider())
