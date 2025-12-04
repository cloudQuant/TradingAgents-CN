"""
可转债分时行情服务（重构版）

数据集合名称: bond_zh_hs_cov_min
"""
from app.services.data_sources.base_service import BaseService
from ..providers.bond_zh_hs_cov_min_provider import BondZhHsCovMinProvider


class BondZhHsCovMinService(BaseService):
    """可转债分时行情服务"""
    
    collection_name = "bond_zh_hs_cov_min"
    provider_class = BondZhHsCovMinProvider
