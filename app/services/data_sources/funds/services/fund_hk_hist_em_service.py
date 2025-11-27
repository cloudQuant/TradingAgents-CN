"""
香港基金历史数据-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_hk_hist_em_provider import FundHkHistEmProvider


class FundHkHistEmService(SimpleService):
    """香港基金历史数据-东财服务"""
    
    collection_name = "fund_hk_hist_em"
    provider_class = FundHkHistEmProvider
