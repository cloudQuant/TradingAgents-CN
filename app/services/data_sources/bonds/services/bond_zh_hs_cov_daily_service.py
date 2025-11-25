"""可转债历史行情服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_zh_hs_cov_daily_provider import BondZhHsCovDailyProvider

class BondZhHsCovDailyService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_zh_hs_cov_daily", BondZhHsCovDailyProvider(), unique_keys=["可转债代码", "date"])
