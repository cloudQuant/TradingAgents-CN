"""可转债强赎-集思录服务"""
from app.services.data_sources.bonds.services.base_bond_service import BaseBondService
from app.services.data_sources.bonds.providers.bond_cb_redeem_jsl_provider import BondCbRedeemJslProvider

class BondCbRedeemJslService(BaseBondService):
    def __init__(self, db):
        super().__init__(db, "bond_cb_redeem_jsl", BondCbRedeemJslProvider(), unique_keys=["代码"])
