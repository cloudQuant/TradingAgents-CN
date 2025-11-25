"""可转债详情-同花顺服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_zh_cov_info_ths_provider import BondZhCovInfoThsProvider

class BondZhCovInfoThsService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_zh_cov_info_ths", BondZhCovInfoThsProvider(), unique_keys=["可转债代码"])
