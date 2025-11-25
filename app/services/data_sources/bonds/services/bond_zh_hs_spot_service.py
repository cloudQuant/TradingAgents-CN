"""沪深债券实时行情服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_zh_hs_spot_provider import BondZhHsSpotProvider

class BondZhHsSpotService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_zh_hs_spot", BondZhHsSpotProvider(), unique_keys=["代码"])
