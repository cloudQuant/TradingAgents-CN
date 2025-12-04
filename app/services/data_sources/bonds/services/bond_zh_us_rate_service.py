"""
中美国债收益率服务（重构版）

数据集合名称: bond_zh_us_rate
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.bond_zh_us_rate_provider import BondZhUsRateProvider


class BondZhUsRateService(SimpleService):
    """中美国债收益率服务"""
    
    collection_name = "bond_zh_us_rate"
    provider_class = BondZhUsRateProvider
