"""
转股价调整记录-集思录数据提供者（重构版）

数据集合名称: bond_cb_adj_logs_jsl
数据唯一标识: 可转债代码, 股东大会日
"""
from app.services.data_sources.base_provider import BaseProvider


class BondCbAdjLogsJslProvider(BaseProvider):
    """转股价调整记录-集思录数据提供者"""
    
    collection_name = "bond_cb_adj_logs_jsl"
    display_name = "转股价调整记录-集思录"
    akshare_func = "bond_cb_adj_logs_jsl"
    unique_keys = ['可转债代码', '股东大会日']
    
    collection_description = "转股价调整记录-集思录数据"
    collection_route = "/bonds/collections/bond_cb_adj_logs_jsl"
    collection_order = 25
    
    field_info = [
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
