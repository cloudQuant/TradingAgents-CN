"""
可转债实时数据-集思录服务（重构版）

需求文档: tests/bonds/requirements/22_可转债实时数据-集思录.md
数据唯一标识: 代码
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.bond_cb_jsl_provider import BondCbJslProvider


class BondCbJslService(SimpleService):
    """可转债实时数据-集思录服务"""
    
    collection_name = "bond_cb_jsl"
    provider_class = BondCbJslProvider
