"""
期货手续费与保证金服务
"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_comm_info_provider import FuturesCommInfoProvider


class FuturesCommInfoService(BaseFuturesService):
    """期货手续费与保证金服务"""
    
    def __init__(self, db: AsyncIOMotorClient):
        provider = FuturesCommInfoProvider()
        super().__init__(db, "futures_comm_info", provider)
