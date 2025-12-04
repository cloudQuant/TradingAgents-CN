"""
可转债转股数据提供者（重构版）

数据集合名称: bond_cov_stock_issue_cninfo
数据唯一标识: 债券代码
"""
from app.services.data_sources.base_provider import SimpleProvider


class BondCovStockIssueCninfoProvider(SimpleProvider):
    """可转债转股数据提供者"""
    
    collection_name = "bond_cov_stock_issue_cninfo"
    display_name = "可转债转股"
    akshare_func = "bond_cov_stock_issue_cninfo"
    unique_keys = ['债券代码']
    
    collection_description = "可转债转股数据"
    collection_route = "/bonds/collections/bond_cov_stock_issue_cninfo"
    collection_order = 32
    
    field_info = [
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
