"""
企业债发行服务（重构版）

数据集合名称: bond_corporate_issue_cninfo
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.bond_corporate_issue_cninfo_provider import BondCorporateIssueCninfoProvider


class BondCorporateIssueCninfoService(SimpleService):
    """企业债发行服务"""
    
    collection_name = "bond_corporate_issue_cninfo"
    provider_class = BondCorporateIssueCninfoProvider
