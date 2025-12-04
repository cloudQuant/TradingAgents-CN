"""
质押式回购历史数据服务（重构版）

数据集合名称: bond_buy_back_hist_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.bond_buy_back_hist_em_provider import BondBuyBackHistEmProvider


class BondBuyBackHistEmService(BaseService):
    """质押式回购历史数据服务"""
    
    collection_name = "bond_buy_back_hist_em"
    provider_class = BondBuyBackHistEmProvider
