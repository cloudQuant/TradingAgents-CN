"""
郑州商品交易所仓单日报服务
"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_warehouse_receipt_czce_provider import FuturesWarehouseReceiptCzceProvider


class FuturesWarehouseReceiptCzceService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        provider = FuturesWarehouseReceiptCzceProvider()
        super().__init__(db, "futures_warehouse_receipt_czce", provider)
