"""外盘合约详情服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_foreign_detail_provider import FuturesForeignDetailProvider

class FuturesForeignDetailService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_foreign_detail", FuturesForeignDetailProvider())
