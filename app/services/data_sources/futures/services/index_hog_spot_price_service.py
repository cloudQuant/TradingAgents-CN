"""生猪市场价格指数服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.index_hog_spot_price_provider import IndexHogSpotPriceProvider

class IndexHogSpotPriceService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "index_hog_spot_price", IndexHogSpotPriceProvider())
