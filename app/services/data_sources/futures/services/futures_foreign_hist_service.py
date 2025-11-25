"""外盘历史行情数据-新浪服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_foreign_hist_provider import FuturesForeignHistProvider

class FuturesForeignHistService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_foreign_hist", FuturesForeignHistProvider())
