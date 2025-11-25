"""期货合约详情-新浪服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_contract_detail_provider import FuturesContractDetailProvider

class FuturesContractDetailService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_contract_detail", FuturesContractDetailProvider())
