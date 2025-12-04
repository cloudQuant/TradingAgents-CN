"""
可转债历史行情-日频服务（重构版）

需求文档: tests/bonds/requirements/06_可转债历史行情-日频.md
数据唯一标识: 可转债代码和日期
"""
from app.services.data_sources.base_service import BaseService
from ..providers.bond_zh_hs_cov_daily_provider import BondZhHsCovDailyProvider


class BondZhHsCovDailyService(BaseService):
    """可转债历史行情-日频服务"""
    
    collection_name = "bond_zh_hs_cov_daily"
    provider_class = BondZhHsCovDailyProvider
