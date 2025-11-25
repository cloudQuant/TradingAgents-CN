"""中证商品指数服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_index_ccidx_provider import FuturesIndexCcidxProvider

class FuturesIndexCcidxService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_index_ccidx", FuturesIndexCcidxProvider())
