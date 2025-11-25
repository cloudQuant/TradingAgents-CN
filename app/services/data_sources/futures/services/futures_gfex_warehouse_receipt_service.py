"""
广州期货交易所仓单日报服务
"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_gfex_warehouse_receipt_provider import FuturesGfexWarehouseReceiptProvider


class FuturesGfexWarehouseReceiptService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        provider = FuturesGfexWarehouseReceiptProvider()
        super().__init__(db, "futures_gfex_warehouse_receipt", provider)
