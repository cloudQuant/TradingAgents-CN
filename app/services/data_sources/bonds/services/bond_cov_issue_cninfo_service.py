"""可转债发行服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_cov_issue_cninfo_provider import BondCovIssueCninfoProvider

class BondCovIssueCninfoService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_cov_issue_cninfo", BondCovIssueCninfoProvider(), unique_keys=["债券简称"])
