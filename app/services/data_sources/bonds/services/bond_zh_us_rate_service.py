"""中美国债收益率服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_zh_us_rate_provider import BondZhUsRateProvider

class BondZhUsRateService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_zh_us_rate", BondZhUsRateProvider(), unique_keys=["日期"])
