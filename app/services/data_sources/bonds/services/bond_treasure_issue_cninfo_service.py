"""国债发行服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_treasure_issue_cninfo_provider import BondTreasureIssueCninfoProvider

class BondTreasureIssueCninfoService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_treasure_issue_cninfo", BondTreasureIssueCninfoProvider(), unique_keys=["债券简称"])
