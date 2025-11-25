"""内盘历史行情数据-交易所服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.get_futures_daily_provider import GetFuturesDailyProvider

class GetFuturesDailyService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "get_futures_daily", GetFuturesDailyProvider())
