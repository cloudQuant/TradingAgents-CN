"""
郑商所期转现服务
"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_to_spot_czce_provider import FuturesToSpotCzceProvider


class FuturesToSpotCzceService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        provider = FuturesToSpotCzceProvider()
        super().__init__(db, "futures_to_spot_czce", provider)
