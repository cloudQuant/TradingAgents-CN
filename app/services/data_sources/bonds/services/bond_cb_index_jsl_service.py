"""可转债等权指数-集思录服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_cb_index_jsl_provider import BondCbIndexJslProvider

class BondCbIndexJslService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_cb_index_jsl", BondCbIndexJslProvider(), unique_keys=["日期"])
