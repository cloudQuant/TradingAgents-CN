"""
现券市场成交行情服务（重构版）

数据集合名称: bond_spot_deal
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.bond_spot_deal_provider import BondSpotDealProvider


class BondSpotDealService(SimpleService):
    """现券市场成交行情服务"""
    
    collection_name = "bond_spot_deal"
    provider_class = BondSpotDealProvider
