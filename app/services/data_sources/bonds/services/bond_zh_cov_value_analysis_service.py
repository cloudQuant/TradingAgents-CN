"""
可转债价值分析服务（重构版）

数据集合名称: bond_zh_cov_value_analysis
批量更新: 从 bond_zh_cov 集合获取债券代码
"""
from typing import Dict, Any
from app.services.data_sources.base_service import BaseService
from ..providers.bond_zh_cov_value_analysis_provider import BondZhCovValueAnalysisProvider


class BondZhCovValueAnalysisService(BaseService):
    """可转债价值分析服务"""
    
    collection_name = "bond_zh_cov_value_analysis"
    provider_class = BondZhCovValueAnalysisProvider
    
    # 批量更新配置：从 bond_zh_cov 集合获取债券代码
    batch_source_collection = "bond_zh_cov"
    batch_source_field = "债券代码"
    
    # 增量更新配置：按代码检查是否已存在数据
    incremental_check_fields = ["代码"]
    
    # 并发配置
    batch_concurrency = 3
    
    def get_batch_params(self, code: str) -> Dict[str, Any]:
        """将债券代码转换为 provider 的 symbol 参数"""
        return {"symbol": code}
