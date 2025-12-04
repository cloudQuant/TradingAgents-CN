"""
上证质押式回购服务（重构版）

数据集合名称: bond_sh_buy_back_em
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.bond_sh_buy_back_em_provider import BondShBuyBackEmProvider


class BondShBuyBackEmService(SimpleService):
    """上证质押式回购服务"""
    
    collection_name = "bond_sh_buy_back_em"
    provider_class = BondShBuyBackEmProvider
