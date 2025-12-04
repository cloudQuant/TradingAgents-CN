"""
沪深债券历史行情服务（重构版）

需求文档: tests/bonds/requirements/04_沪深债券历史行情.md
数据唯一标识: 债券代码和日期
"""
from app.services.data_sources.base_service import BaseService
from ..providers.bond_zh_hs_daily_provider import BondZhHsDailyProvider


class BondZhHsDailyService(BaseService):
    """沪深债券历史行情服务"""
    
    collection_name = "bond_zh_hs_daily"
    provider_class = BondZhHsDailyProvider
