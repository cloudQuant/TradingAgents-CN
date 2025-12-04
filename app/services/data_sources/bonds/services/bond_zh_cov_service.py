"""
可转债数据一览表-东财服务（重构版：继承SimpleService）

需求文档: tests/bonds/requirements/07_可转债数据一览表-东财.md
数据唯一标识: 债券代码
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.bond_zh_cov_provider import BondZhCovProvider


class BondZhCovService(SimpleService):
    """可转债数据一览表-东财服务"""
    
    collection_name = "bond_zh_cov"
    provider_class = BondZhCovProvider
