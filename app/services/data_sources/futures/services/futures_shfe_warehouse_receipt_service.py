"""
上海期货交易所仓单日报服务
"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_shfe_warehouse_receipt_provider import FuturesShfeWarehouseReceiptProvider


class FuturesShfeWarehouseReceiptService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        provider = FuturesShfeWarehouseReceiptProvider()
        super().__init__(db, "futures_shfe_warehouse_receipt", provider)
