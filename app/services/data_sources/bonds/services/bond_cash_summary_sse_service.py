"""债券现券市场概览服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_cash_summary_sse_provider import BondCashSummarySseProvider

class BondCashSummarySseService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_cash_summary_sse", BondCashSummarySseProvider(), unique_keys=["查询日期", "债券现货"])
