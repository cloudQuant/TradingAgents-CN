"""内盘历史行情数据-新浪服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_zh_daily_sina_provider import FuturesZhDailySinaProvider

class FuturesZhDailySinaService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_zh_daily_sina", FuturesZhDailySinaProvider())
