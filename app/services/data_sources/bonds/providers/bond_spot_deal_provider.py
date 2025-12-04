"""
现券市场成交行情数据提供者（重构版）

数据集合名称: bond_spot_deal
数据唯一标识: 债券简称
"""
from app.services.data_sources.base_provider import SimpleProvider


class BondSpotDealProvider(SimpleProvider):
    """现券市场成交行情数据提供者"""
    
    collection_name = "bond_spot_deal"
    display_name = "现券市场成交行情"
    akshare_func = "bond_spot_deal"
    unique_keys = ['债券简称']
    
    collection_description = "现券市场成交行情数据"
    collection_route = "/bonds/collections/bond_spot_deal"
    collection_order = 12
    
    field_info = [
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
