"""
平衡型基金仓位-理杏仁服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_balance_position_lg_provider import FundBalancePositionLgProvider


class FundBalancePositionLgService(SimpleService):
    """平衡型基金仓位-理杏仁服务"""
    
    collection_name = "fund_balance_position_lg"
    provider_class = FundBalancePositionLgProvider
