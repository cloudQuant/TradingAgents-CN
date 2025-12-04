"""
现券市场做市报价数据提供者（重构版）

数据集合名称: bond_spot_quote
数据唯一标识: 报价机构, 债券简称
"""
from app.services.data_sources.base_provider import SimpleProvider


class BondSpotQuoteProvider(SimpleProvider):
    """现券市场做市报价数据提供者"""
    
    collection_name = "bond_spot_quote"
    display_name = "现券市场做市报价"
    akshare_func = "bond_spot_quote"
    unique_keys = ['报价机构', '债券简称']
    
    collection_description = "现券市场做市报价数据"
    collection_route = "/bonds/collections/bond_spot_quote"
    collection_order = 11
    
    field_info = [
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
