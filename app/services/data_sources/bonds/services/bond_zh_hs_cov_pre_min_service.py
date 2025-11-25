"""可转债盘前分时服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_zh_hs_cov_pre_min_provider import BondZhHsCovPreMinProvider

class BondZhHsCovPreMinService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_zh_hs_cov_pre_min", BondZhHsCovPreMinProvider(), unique_keys=["可转债代码", "时间"])
