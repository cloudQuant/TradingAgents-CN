"""债券成交概览服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_deal_summary_sse_provider import BondDealSummarySseProvider

class BondDealSummarySseService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_deal_summary_sse", BondDealSummarySseProvider(), unique_keys=["查询日期", "债券类型"])
