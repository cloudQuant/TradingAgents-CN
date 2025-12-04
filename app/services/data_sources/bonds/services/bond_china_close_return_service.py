"""
收益率曲线历史数据服务（重构版）

数据集合名称: bond_china_close_return
"""
from app.services.data_sources.base_service import BaseService
from ..providers.bond_china_close_return_provider import BondChinaCloseReturnProvider


class BondChinaCloseReturnService(BaseService):
    """收益率曲线历史数据服务"""
    
    collection_name = "bond_china_close_return"
    provider_class = BondChinaCloseReturnProvider
