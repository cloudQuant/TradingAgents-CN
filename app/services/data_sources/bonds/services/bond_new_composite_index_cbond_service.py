"""
中债新综合指数服务（重构版）

数据集合名称: bond_new_composite_index_cbond
"""
from app.services.data_sources.base_service import BaseService
from ..providers.bond_new_composite_index_cbond_provider import BondNewCompositeIndexCbondProvider


class BondNewCompositeIndexCbondService(BaseService):
    """中债新综合指数服务"""
    
    collection_name = "bond_new_composite_index_cbond"
    provider_class = BondNewCompositeIndexCbondProvider
