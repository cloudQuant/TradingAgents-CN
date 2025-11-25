"""外盘历史行情数据-东财服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_global_hist_em_provider import FuturesGlobalHistEmProvider

class FuturesGlobalHistEmService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_global_hist_em", FuturesGlobalHistEmProvider())
