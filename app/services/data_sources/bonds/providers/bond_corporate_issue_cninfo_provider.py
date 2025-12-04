"""
企业债发行数据提供者（重构版）

数据集合名称: bond_corporate_issue_cninfo
数据唯一标识: 债券代码
"""
from app.services.data_sources.base_provider import SimpleProvider


class BondCorporateIssueCninfoProvider(SimpleProvider):
    """企业债发行数据提供者"""
    
    collection_name = "bond_corporate_issue_cninfo"
    display_name = "企业债发行"
    akshare_func = "bond_corporate_issue_cninfo"
    unique_keys = ['债券代码']
    
    collection_description = "企业债发行数据"
    collection_route = "/bonds/collections/bond_corporate_issue_cninfo"
    collection_order = 30
    
    field_info = [
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
