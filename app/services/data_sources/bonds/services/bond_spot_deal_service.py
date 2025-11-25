"""现券市场成交行情服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_spot_deal_provider import BondSpotDealProvider

class BondSpotDealService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_spot_deal", BondSpotDealProvider(), unique_keys=["债券简称"])
