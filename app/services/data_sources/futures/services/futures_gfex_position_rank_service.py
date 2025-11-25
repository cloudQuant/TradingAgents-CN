"""
广州期货交易所持仓排名服务
"""
from motor.motor_asyncio import AsyncIOMotorClient
from .base_futures_service import BaseFuturesService
from ..providers.futures_gfex_position_rank_provider import FuturesGfexPositionRankProvider


class FuturesGfexPositionRankService(BaseFuturesService):
    def __init__(self, db: AsyncIOMotorClient):
        provider = FuturesGfexPositionRankProvider()
        super().__init__(db, "futures_gfex_position_rank", provider)
