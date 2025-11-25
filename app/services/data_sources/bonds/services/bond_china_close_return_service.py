"""收益率曲线历史数据服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_china_close_return_provider import BondChinaCloseReturnProvider

class BondChinaCloseReturnService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_china_close_return", BondChinaCloseReturnProvider(), unique_keys=["日期"])
