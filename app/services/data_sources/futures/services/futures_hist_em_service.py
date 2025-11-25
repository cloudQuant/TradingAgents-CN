"""内盘历史行情数据-东财服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_hist_em_provider import FuturesHistEmProvider

class FuturesHistEmService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_hist_em", FuturesHistEmProvider())
