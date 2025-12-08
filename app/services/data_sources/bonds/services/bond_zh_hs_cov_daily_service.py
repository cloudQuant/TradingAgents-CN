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

    # 批量更新：从实时行情集合中按 symbol（带交易所前缀，如 sh110044、sz128039）驱动
    batch_source_collection = "bond_zh_hs_cov_spot"
    batch_source_field = "symbol"

    def get_batch_params(self, symbol):
        """根据可转债 symbol 构造 Provider 调用参数"""
        if symbol:
            return {"symbol": symbol}
        return {}
