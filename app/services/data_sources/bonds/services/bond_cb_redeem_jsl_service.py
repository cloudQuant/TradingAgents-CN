"""
可转债强赎-集思录服务（重构版）

数据集合名称: bond_cb_redeem_jsl
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.bond_cb_redeem_jsl_provider import BondCbRedeemJslProvider


class BondCbRedeemJslService(SimpleService):
    """可转债强赎-集思录服务"""
    
    collection_name = "bond_cb_redeem_jsl"
    provider_class = BondCbRedeemJslProvider
