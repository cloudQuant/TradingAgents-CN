"""
期货规则-交易日历表服务
"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_rule_provider import FuturesRuleProvider


class FuturesRuleService(BaseFuturesService):
    """期货规则-交易日历表服务"""
    
    def __init__(self, db: AsyncIOMotorClient):
        provider = FuturesRuleProvider()
        super().__init__(db, "futures_rule", provider)
