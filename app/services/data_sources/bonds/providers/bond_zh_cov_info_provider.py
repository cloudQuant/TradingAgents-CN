"""
可转债详情-东财数据提供者（重构版）

数据集合名称: bond_zh_cov_info
数据唯一标识: 可转债代码, item
"""
from app.services.data_sources.base_provider import BaseProvider


class BondZhCovInfoProvider(BaseProvider):
    """可转债详情-东财数据提供者"""
    
    collection_name = "bond_zh_cov_info"
    display_name = "可转债详情-东财"
    akshare_func = "bond_zh_cov_info"
    unique_keys = ['可转债代码', 'item']
    
    collection_description = "可转债详情-东财数据"
    collection_route = "/bonds/collections/bond_zh_cov_info"
    collection_order = 15
    
    field_info = [
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
