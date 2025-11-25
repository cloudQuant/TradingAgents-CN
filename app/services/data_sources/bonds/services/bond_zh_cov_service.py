"""可转债数据一览表服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_zh_cov_provider import BondZhCovProvider

class BondZhCovService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_zh_cov", BondZhCovProvider(), unique_keys=["债券代码"])
