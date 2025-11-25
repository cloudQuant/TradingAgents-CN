"""可转债转股服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_cov_stock_issue_cninfo_provider import BondCovStockIssueCninfoProvider

class BondCovStockIssueCninfoService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_cov_stock_issue_cninfo", BondCovStockIssueCninfoProvider(), unique_keys=["债券简称"])
