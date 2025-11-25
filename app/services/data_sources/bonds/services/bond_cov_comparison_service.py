"""可转债比价表服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_cov_comparison_provider import BondCovComparisonProvider

class BondCovComparisonService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_cov_comparison", BondCovComparisonProvider(), unique_keys=["转债代码"])
