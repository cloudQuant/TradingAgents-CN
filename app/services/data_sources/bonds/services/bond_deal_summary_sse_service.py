"""
债券成交概览-上交所服务（重构版）

数据集合名称: bond_deal_summary_sse
"""
from app.services.data_sources.base_service import BaseService
from ..providers.bond_deal_summary_sse_provider import BondDealSummarySseProvider


class BondDealSummarySseService(BaseService):
    """债券成交概览-上交所服务"""
    
    collection_name = "bond_deal_summary_sse"
    provider_class = BondDealSummarySseProvider
