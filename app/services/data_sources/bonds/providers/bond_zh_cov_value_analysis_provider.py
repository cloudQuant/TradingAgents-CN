"""
可转债价值分析数据提供者（重构版）

数据集合名称: bond_zh_cov_value_analysis
数据唯一标识: 可转债代码, 日期
"""
from app.services.data_sources.base_provider import BaseProvider


class BondZhCovValueAnalysisProvider(BaseProvider):
    """可转债价值分析数据提供者"""
    
    collection_name = "bond_zh_cov_value_analysis"
    display_name = "可转债价值分析"
    akshare_func = "bond_zh_cov_value_analysis"
    unique_keys = ['可转债代码', '日期']
    
    collection_description = "可转债价值分析数据"
    collection_route = "/bonds/collections/bond_zh_cov_value_analysis"
    collection_order = 18
    
    field_info = [
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
