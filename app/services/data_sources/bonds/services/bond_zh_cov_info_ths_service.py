"""
可转债详情-同花顺服务（重构版）

数据集合名称: bond_zh_cov_info_ths
"""
from app.services.data_sources.base_service import BaseService
from ..providers.bond_zh_cov_info_ths_provider import BondZhCovInfoThsProvider


class BondZhCovInfoThsService(BaseService):
    """可转债详情-同花顺服务"""
    
    collection_name = "bond_zh_cov_info_ths"
    provider_class = BondZhCovInfoThsProvider
