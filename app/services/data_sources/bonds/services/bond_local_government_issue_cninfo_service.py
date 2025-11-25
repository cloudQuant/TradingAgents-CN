"""地方债发行服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_local_government_issue_cninfo_provider import BondLocalGovernmentIssueCninfoProvider

class BondLocalGovernmentIssueCninfoService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_local_government_issue_cninfo", BondLocalGovernmentIssueCninfoProvider(), unique_keys=["债券简称"])
