"""
沪深债券实时行情服务（重构版：继承SimpleService）

需求文档: tests/bonds/requirements/03_沪深债券实时行情.md
数据唯一标识: 代码
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.bond_zh_hs_spot_provider import BondZhHsSpotProvider


class BondZhHsSpotService(SimpleService):
    """沪深债券实时行情服务"""
    
    collection_name = "bond_zh_hs_spot"
    provider_class = BondZhHsSpotProvider
