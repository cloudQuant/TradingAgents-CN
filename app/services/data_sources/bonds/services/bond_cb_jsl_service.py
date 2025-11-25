"""可转债实时数据-集思录服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_cb_jsl_provider import BondCbJslProvider

class BondCbJslService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_cb_jsl", BondCbJslProvider(), unique_keys=["转债代码"])
