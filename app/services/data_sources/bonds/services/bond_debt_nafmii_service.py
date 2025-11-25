"""银行间市场债券发行服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_debt_nafmii_provider import BondDebtNafmiiProvider

class BondDebtNafmiiService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_debt_nafmii", BondDebtNafmiiProvider(), unique_keys=["注册通知书文号"])
