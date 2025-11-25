"""中国金融期货交易所合约信息服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_contract_info_cffex_provider import FuturesContractInfoCffexProvider

class FuturesContractInfoCffexService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_contract_info_cffex", FuturesContractInfoCffexProvider())
