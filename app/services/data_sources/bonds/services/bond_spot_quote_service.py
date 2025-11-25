"""现券市场做市报价服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_spot_quote_provider import BondSpotQuoteProvider

class BondSpotQuoteService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_spot_quote", BondSpotQuoteProvider(), unique_keys=["债券简称", "报价机构"])
