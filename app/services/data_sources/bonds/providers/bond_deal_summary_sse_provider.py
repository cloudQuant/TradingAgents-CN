"""
债券成交概览-上交所数据提供者（重构版）

数据集合名称: bond_deal_summary_sse
数据唯一标识: 债券类型, 数据日期
"""
from app.services.data_sources.base_provider import BaseProvider


class BondDealSummarySseProvider(BaseProvider):
    """债券成交概览-上交所数据提供者"""
    
    collection_name = "bond_deal_summary_sse"
    display_name = "债券成交概览-上交所"
    akshare_func = "bond_deal_summary_sse"
    unique_keys = ['债券类型', '数据日期']
    
    collection_description = "债券成交概览-上交所数据"
    collection_route = "/bonds/collections/bond_deal_summary_sse"
    collection_order = 9
    
    field_info = [
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
