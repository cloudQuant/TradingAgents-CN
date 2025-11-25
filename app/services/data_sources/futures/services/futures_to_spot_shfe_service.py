"""
上期所期转现服务
"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_to_spot_shfe_provider import FuturesToSpotShfeProvider


class FuturesToSpotShfeService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        provider = FuturesToSpotShfeProvider()
        super().__init__(db, "futures_to_spot_shfe", provider)
