"""
债券现券市场概览-上交所数据提供者（重构版）

数据集合名称: bond_cash_summary_sse
数据唯一标识: 债券现货, 数据日期
"""
from app.services.data_sources.base_provider import BaseProvider


class BondCashSummarySseProvider(BaseProvider):
    """债券现券市场概览-上交所数据提供者"""
    
    collection_name = "bond_cash_summary_sse"
    display_name = "债券现券市场概览-上交所"
    akshare_func = "bond_cash_summary_sse"
    unique_keys = ['债券现货', '数据日期']
    
    collection_description = "债券现券市场概览-上交所数据"
    collection_route = "/bonds/collections/bond_cash_summary_sse"
    collection_order = 8
    
    field_info = [
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
