"""
中债综合指数服务（重构版）

数据集合名称: bond_composite_index_cbond
"""
from app.services.data_sources.base_service import BaseService
from ..providers.bond_composite_index_cbond_provider import BondCompositeIndexCbondProvider


class BondCompositeIndexCbondService(BaseService):
    """中债综合指数服务"""
    
    collection_name = "bond_composite_index_cbond"
    provider_class = BondCompositeIndexCbondProvider
