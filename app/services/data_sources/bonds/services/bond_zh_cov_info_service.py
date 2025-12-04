"""
可转债详情-东财服务（重构版）

数据集合名称: bond_zh_cov_info
"""
from app.services.data_sources.base_service import BaseService
from ..providers.bond_zh_cov_info_provider import BondZhCovInfoProvider


class BondZhCovInfoService(BaseService):
    """可转债详情-东财服务"""
    
    collection_name = "bond_zh_cov_info"
    provider_class = BondZhCovInfoProvider
