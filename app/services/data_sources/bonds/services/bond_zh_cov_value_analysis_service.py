"""
可转债价值分析服务（重构版）

数据集合名称: bond_zh_cov_value_analysis
"""
from app.services.data_sources.base_service import BaseService
from ..providers.bond_zh_cov_value_analysis_provider import BondZhCovValueAnalysisProvider


class BondZhCovValueAnalysisService(BaseService):
    """可转债价值分析服务"""
    
    collection_name = "bond_zh_cov_value_analysis"
    provider_class = BondZhCovValueAnalysisProvider
