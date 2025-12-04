"""
可转债强赎-集思录数据提供者（重构版）

数据集合名称: bond_cb_redeem_jsl
数据唯一标识: 代码
"""
from app.services.data_sources.base_provider import SimpleProvider


class BondCbRedeemJslProvider(SimpleProvider):
    """可转债强赎-集思录数据提供者"""
    
    collection_name = "bond_cb_redeem_jsl"
    display_name = "可转债强赎-集思录"
    akshare_func = "bond_cb_redeem_jsl"
    unique_keys = ['代码']
    
    collection_description = "可转债强赎-集思录数据"
    collection_route = "/bonds/collections/bond_cb_redeem_jsl"
    collection_order = 23
    
    field_info = [
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
