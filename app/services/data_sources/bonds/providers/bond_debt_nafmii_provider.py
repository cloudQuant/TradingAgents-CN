"""
银行间市场债券发行数据数据提供者（重构版）

数据集合名称: bond_debt_nafmii
数据唯一标识: 注册通知书文号
"""
from app.services.data_sources.base_provider import SimpleProvider


class BondDebtNafmiiProvider(SimpleProvider):
    """银行间市场债券发行数据数据提供者"""
    
    collection_name = "bond_debt_nafmii"
    display_name = "银行间市场债券发行数据"
    akshare_func = "bond_debt_nafmii"
    unique_keys = ['注册通知书文号']
    
    collection_description = "银行间市场债券发行数据数据"
    collection_route = "/bonds/collections/bond_debt_nafmii"
    collection_order = 10
    
    field_info = [
        {"name": "更新时间", "type": "datetime", "description": "数据更新时间"},
        {"name": "来源", "type": "string", "description": "来源接口"},
    ]
