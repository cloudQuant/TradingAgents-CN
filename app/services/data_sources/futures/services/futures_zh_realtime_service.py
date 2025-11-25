"""内盘实时行情数据(品种)服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_zh_realtime_provider import FuturesZhRealtimeProvider

class FuturesZhRealtimeService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_zh_realtime", FuturesZhRealtimeProvider())
