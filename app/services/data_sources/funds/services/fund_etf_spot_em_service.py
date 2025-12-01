"""
ETF实时行情-东财服务（重构版：继承SimpleService）
"""
from typing import Any, Dict, List

from app.services.data_sources.base_service import SimpleService
from ..providers.fund_etf_spot_em_provider import FundEtfSpotEmProvider


class FundEtfSpotEmService(SimpleService):
    """ETF实时行情-东财服务"""
    
    collection_name = "fund_etf_spot_em"
    provider_class = FundEtfSpotEmProvider

    # 使用基类的默认 get_overview 方法，只返回基本统计
    # 不再提供市场概况相关的统计数据
