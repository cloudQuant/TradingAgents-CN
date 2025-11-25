"""期货合约详情-东财服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_contract_detail_em_provider import FuturesContractDetailEmProvider

class FuturesContractDetailEmService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_contract_detail_em", FuturesContractDetailEmProvider())
