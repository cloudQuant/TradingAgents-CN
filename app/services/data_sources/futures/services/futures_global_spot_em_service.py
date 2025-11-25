"""外盘实时行情数据-东财服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_global_spot_em_provider import FuturesGlobalSpotEmProvider

class FuturesGlobalSpotEmService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_global_spot_em", FuturesGlobalSpotEmProvider())
