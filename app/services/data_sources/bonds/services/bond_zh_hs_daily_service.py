"""沪深债券历史行情服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_zh_hs_daily_provider import BondZhHsDailyProvider

class BondZhHsDailyService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_zh_hs_daily", BondZhHsDailyProvider(), unique_keys=["债券代码", "date"])
