"""转股价调整记录-集思录服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_cb_adj_logs_jsl_provider import BondCbAdjLogsJslProvider

class BondCbAdjLogsJslService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_cb_adj_logs_jsl", BondCbAdjLogsJslProvider(), unique_keys=["可转债代码", "调整日期"])
