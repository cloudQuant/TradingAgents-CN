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
    unique_keys = ['代码',"更新时间"]
    
    collection_description = "可转债强赎-集思录数据"
    collection_route = "/bonds/collections/bond_cb_redeem_jsl"
    collection_order = 23
    
    field_info = [
        {"name": "代码", "type": "string", "description": "可转债代码"},
        {"name": "名称", "type": "string", "description": "可转债名称"},
        {"name": "现价", "type": "float", "description": "可转债现价"},
        {"name": "正股代码", "type": "string", "description": "正股代码"},
        {"name": "正股名称", "type": "string", "description": "正股名称"},
        {"name": "规模", "type": "float", "description": "可转债发行规模，单位：亿"},
        {"name": "剩余规模", "type": "float", "description": "剩余规模，单位：亿"},
        {"name": "转股起始日", "type": "string", "description": "转股起始日"},
        {"name": "最后交易日", "type": "string", "description": "最后交易日"},
        {"name": "到期日", "type": "string", "description": "到期日"},
        {"name": "转股价", "type": "float", "description": "转股价格"},
        {"name": "强赎触发比", "type": "float", "description": "强赎触发比(%)"},
        {"name": "强赎触发价", "type": "float", "description": "强赎触发价"},
        {"name": "正股价", "type": "float", "description": "正股当前价格"},
        {"name": "强赎价", "type": "float", "description": "强赎价格"},
        {"name": "强赎天计数", "type": "string", "description": "强赎天计数，如 \"25/15 | 30\""},
        {"name": "强赎条款", "type": "string", "description": "强赎条款"},
        {"name": "强赎状态", "type": "string", "description": "强赎状态"},
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
