"""上海期货交易所合约信息服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_contract_info_shfe_provider import FuturesContractInfoShfeProvider

class FuturesContractInfoShfeService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_contract_info_shfe", FuturesContractInfoShfeProvider())
