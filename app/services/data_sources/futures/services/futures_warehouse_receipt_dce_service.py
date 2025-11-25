"""
大连商品交易所仓单日报服务
"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_warehouse_receipt_dce_provider import FuturesWarehouseReceiptDceProvider


class FuturesWarehouseReceiptDceService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        provider = FuturesWarehouseReceiptDceProvider()
        super().__init__(db, "futures_warehouse_receipt_dce", provider)
