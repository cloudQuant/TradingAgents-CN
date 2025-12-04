"""
可转债详情-同花顺数据提供者（重构版）

数据集合名称: bond_zh_cov_info_ths
数据唯一标识: 债券代码
"""
from app.services.data_sources.base_provider import BaseProvider


class BondZhCovInfoThsProvider(BaseProvider):
    """可转债详情-同花顺数据提供者"""
    
    collection_name = "bond_zh_cov_info_ths"
    display_name = "可转债详情-同花顺"
    akshare_func = "bond_zh_cov_info_ths"
    unique_keys = ['债券代码']
    
    collection_description = "可转债详情-同花顺数据"
    collection_route = "/bonds/collections/bond_zh_cov_info_ths"
    collection_order = 16
    
    field_info = [
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
