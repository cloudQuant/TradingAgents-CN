"""
期货交易费用参照表服务
"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_fees_info_provider import FuturesFeesInfoProvider


class FuturesFeesInfoService(BaseFuturesService):
    """期货交易费用参照表服务"""
    
    def __init__(self, db: AsyncIOMotorClient):
        provider = FuturesFeesInfoProvider()
        super().__init__(db, "futures_fees_info", provider)
