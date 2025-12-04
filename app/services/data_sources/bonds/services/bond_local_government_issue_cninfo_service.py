"""
地方债发行服务（重构版）

数据集合名称: bond_local_government_issue_cninfo
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.bond_local_government_issue_cninfo_provider import BondLocalGovernmentIssueCninfoProvider


class BondLocalGovernmentIssueCninfoService(SimpleService):
    """地方债发行服务"""
    
    collection_name = "bond_local_government_issue_cninfo"
    provider_class = BondLocalGovernmentIssueCninfoProvider
