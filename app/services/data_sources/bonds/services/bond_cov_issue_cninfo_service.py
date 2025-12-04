"""
可转债发行服务（重构版）

数据集合名称: bond_cov_issue_cninfo
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.bond_cov_issue_cninfo_provider import BondCovIssueCninfoProvider


class BondCovIssueCninfoService(SimpleService):
    """可转债发行服务"""
    
    collection_name = "bond_cov_issue_cninfo"
    provider_class = BondCovIssueCninfoProvider
