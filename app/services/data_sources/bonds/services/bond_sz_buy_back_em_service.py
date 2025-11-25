"""深证质押式回购服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_sz_buy_back_em_provider import BondSzBuyBackEmProvider

class BondSzBuyBackEmService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_sz_buy_back_em", BondSzBuyBackEmProvider(), unique_keys=["代码"])
