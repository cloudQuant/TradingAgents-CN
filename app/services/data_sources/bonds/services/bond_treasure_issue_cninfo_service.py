"""
国债发行服务（重构版）

数据集合名称: bond_treasure_issue_cninfo
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.bond_treasure_issue_cninfo_provider import BondTreasureIssueCninfoProvider


class BondTreasureIssueCninfoService(SimpleService):
    """国债发行服务"""
    
    collection_name = "bond_treasure_issue_cninfo"
    provider_class = BondTreasureIssueCninfoProvider
