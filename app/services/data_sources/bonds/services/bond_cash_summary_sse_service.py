"""
债券现券市场概览-上交所服务（重构版）

数据集合名称: bond_cash_summary_sse
"""
from app.services.data_sources.base_service import BaseService
from ..providers.bond_cash_summary_sse_provider import BondCashSummarySseProvider


class BondCashSummarySseService(BaseService):
    """债券现券市场概览-上交所服务"""
    
    collection_name = "bond_cash_summary_sse"
    provider_class = BondCashSummarySseProvider
