"""
债券查询-中国外汇交易中心服务（重构版：继承SimpleService）

需求文档: tests/bonds/requirements/01_债券查询-中国外汇交易中心.md
数据唯一标识: 查询代码
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.bond_info_cm_provider import BondInfoCmProvider


class BondInfoCmService(SimpleService):
    """债券查询-中国外汇交易中心服务"""
    
    collection_name = "bond_info_cm"
    provider_class = BondInfoCmProvider
