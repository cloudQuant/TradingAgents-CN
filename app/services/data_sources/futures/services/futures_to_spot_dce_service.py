"""
大商所期转现服务
"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_to_spot_dce_provider import FuturesToSpotDceProvider


class FuturesToSpotDceService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        provider = FuturesToSpotDceProvider()
        super().__init__(db, "futures_to_spot_dce", provider)
