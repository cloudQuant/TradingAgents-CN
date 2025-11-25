"""内盘分时行情数据服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_zh_minute_sina_provider import FuturesZhMinuteSinaProvider

class FuturesZhMinuteSinaService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_zh_minute_sina", FuturesZhMinuteSinaProvider())
