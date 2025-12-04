"""
现券市场做市报价服务（重构版）

数据集合名称: bond_spot_quote
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.bond_spot_quote_provider import BondSpotQuoteProvider


class BondSpotQuoteService(SimpleService):
    """现券市场做市报价服务"""
    
    collection_name = "bond_spot_quote"
    provider_class = BondSpotQuoteProvider
