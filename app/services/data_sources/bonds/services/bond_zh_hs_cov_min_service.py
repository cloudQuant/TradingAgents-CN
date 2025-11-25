"""可转债分时行情服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_zh_hs_cov_min_provider import BondZhHsCovMinProvider

class BondZhHsCovMinService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_zh_hs_cov_min", BondZhHsCovMinProvider(), unique_keys=["可转债代码", "时间"])
