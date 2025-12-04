"""
可转债实时行情-沪深服务（重构版：继承SimpleService）

需求文档: tests/bonds/requirements/05_可转债实时行情-沪深.md
数据唯一标识: 代码
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.bond_zh_hs_cov_spot_provider import BondZhHsCovSpotProvider


class BondZhHsCovSpotService(SimpleService):
    """可转债实时行情-沪深服务"""
    
    collection_name = "bond_zh_hs_cov_spot"
    provider_class = BondZhHsCovSpotProvider
