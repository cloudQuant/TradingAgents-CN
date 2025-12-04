"""
深证质押式回购数据提供者（重构版）

数据集合名称: bond_sz_buy_back_em
数据唯一标识: 代码
"""
from app.services.data_sources.base_provider import SimpleProvider


class BondSzBuyBackEmProvider(SimpleProvider):
    """深证质押式回购数据提供者"""
    
    collection_name = "bond_sz_buy_back_em"
    display_name = "深证质押式回购"
    akshare_func = "bond_repurchase_em"
    unique_keys = ['代码']
    
    collection_description = "深证质押式回购数据"
    collection_route = "/bonds/collections/bond_sz_buy_back_em"
    collection_order = 20
    
    field_info = [
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
