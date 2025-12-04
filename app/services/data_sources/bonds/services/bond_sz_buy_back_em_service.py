"""
深证质押式回购服务（重构版）

数据集合名称: bond_sz_buy_back_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.bond_sz_buy_back_em_provider import BondSzBuyBackEmProvider


class BondSzBuyBackEmService(SimpleService):
    """深证质押式回购服务"""
    
    collection_name = "bond_sz_buy_back_em"
    provider_class = BondSzBuyBackEmProvider
