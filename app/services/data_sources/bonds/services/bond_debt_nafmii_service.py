"""
银行间市场债券发行数据服务（重构版）

数据集合名称: bond_debt_nafmii
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.bond_debt_nafmii_provider import BondDebtNafmiiProvider


class BondDebtNafmiiService(SimpleService):
    """银行间市场债券发行数据服务"""
    
    collection_name = "bond_debt_nafmii"
    provider_class = BondDebtNafmiiProvider
