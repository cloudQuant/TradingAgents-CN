"""
可转债等权指数-集思录服务（重构版）

数据集合名称: bond_cb_index_jsl
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.bond_cb_index_jsl_provider import BondCbIndexJslProvider


class BondCbIndexJslService(SimpleService):
    """可转债等权指数-集思录服务"""
    
    collection_name = "bond_cb_index_jsl"
    provider_class = BondCbIndexJslProvider
