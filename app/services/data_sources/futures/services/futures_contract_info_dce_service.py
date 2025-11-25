"""大连商品交易所合约信息服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_contract_info_dce_provider import FuturesContractInfoDceProvider

class FuturesContractInfoDceService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_contract_info_dce", FuturesContractInfoDceProvider())
