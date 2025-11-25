"""外盘实时行情数据服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_foreign_commodity_realtime_provider import FuturesForeignCommodityRealtimeProvider

class FuturesForeignCommodityRealtimeService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_foreign_commodity_realtime", FuturesForeignCommodityRealtimeProvider())
