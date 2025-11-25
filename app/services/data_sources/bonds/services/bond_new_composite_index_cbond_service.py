"""中债新综合指数服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_new_composite_index_cbond_provider import BondNewCompositeIndexCbondProvider

class BondNewCompositeIndexCbondService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_new_composite_index_cbond", BondNewCompositeIndexCbondProvider(), unique_keys=["日期"])
