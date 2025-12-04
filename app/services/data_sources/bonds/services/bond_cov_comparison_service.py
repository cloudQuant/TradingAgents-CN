"""
可转债比价表服务（重构版）

数据集合名称: bond_cov_comparison
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.bond_cov_comparison_provider import BondCovComparisonProvider


class BondCovComparisonService(SimpleService):
    """可转债比价表服务"""
    
    collection_name = "bond_cov_comparison"
    provider_class = BondCovComparisonProvider
