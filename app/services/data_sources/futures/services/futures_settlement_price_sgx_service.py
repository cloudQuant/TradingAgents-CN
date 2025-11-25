"""新加坡交易所期货服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_settlement_price_sgx_provider import FuturesSettlementPriceSgxProvider

class FuturesSettlementPriceSgxService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_settlement_price_sgx", FuturesSettlementPriceSgxProvider())
