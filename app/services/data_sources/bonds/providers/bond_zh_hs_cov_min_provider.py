"""
可转债分时行情数据提供者（重构版）

数据集合名称: bond_zh_hs_cov_min
数据唯一标识: 可转债代码, 时间
"""
from app.services.data_sources.base_provider import BaseProvider


class BondZhHsCovMinProvider(BaseProvider):
    """可转债分时行情数据提供者"""
    
    collection_name = "bond_zh_hs_cov_min"
    display_name = "可转债分时行情"
    akshare_func = "bond_zh_hs_cov_min"
    unique_keys = ['可转债代码', '时间']
    
    collection_description = "可转债分时行情数据"
    collection_route = "/bonds/collections/bond_zh_hs_cov_min"
    collection_order = 13
    
    field_info = [
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
