"""
中债综合指数数据提供者（重构版）

数据集合名称: bond_composite_index_cbond
数据唯一标识: 指标类型, 期限, date
"""
from app.services.data_sources.base_provider import BaseProvider


class BondCompositeIndexCbondProvider(BaseProvider):
    """中债综合指数数据提供者"""
    
    collection_name = "bond_composite_index_cbond"
    display_name = "中债综合指数"
    akshare_func = "bond_index_cbond"
    unique_keys = ['指标类型', '期限', 'date']
    
    collection_description = "中债综合指数数据"
    collection_route = "/bonds/collections/bond_composite_index_cbond"
    collection_order = 34
    
    field_info = [
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
