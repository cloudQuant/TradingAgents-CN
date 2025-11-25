"""可转债实时行情服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_zh_hs_cov_spot_provider import BondZhHsCovSpotProvider

class BondZhHsCovSpotService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_zh_hs_cov_spot", BondZhHsCovSpotProvider(), unique_keys=["代码"])
