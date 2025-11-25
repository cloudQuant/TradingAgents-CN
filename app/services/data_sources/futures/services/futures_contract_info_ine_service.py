"""上海国际能源交易中心合约信息服务"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_contract_info_ine_provider import FuturesContractInfoIneProvider

class FuturesContractInfoIneService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        super().__init__(db, "futures_contract_info_ine", FuturesContractInfoIneProvider())
