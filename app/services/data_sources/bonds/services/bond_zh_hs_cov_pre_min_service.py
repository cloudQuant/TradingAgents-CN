"""
可转债盘前分时服务（重构版）

数据集合名称: bond_zh_hs_cov_pre_min
"""
from app.services.data_sources.base_service import BaseService
from ..providers.bond_zh_hs_cov_pre_min_provider import BondZhHsCovPreMinProvider


class BondZhHsCovPreMinService(BaseService):
    """可转债盘前分时服务"""
    
    collection_name = "bond_zh_hs_cov_pre_min"
    provider_class = BondZhHsCovPreMinProvider
