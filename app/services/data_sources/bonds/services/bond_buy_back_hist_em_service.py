"""质押式回购历史数据服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_buy_back_hist_em_provider import BondBuyBackHistEmProvider

class BondBuyBackHistEmService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_buy_back_hist_em", BondBuyBackHistEmProvider(), unique_keys=["回购代码", "日期"])
