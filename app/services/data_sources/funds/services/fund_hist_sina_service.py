"""
基金历史行情-新浪服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_hist_sina_provider import FundHistSinaProvider


class FundHistSinaService(SimpleService):
    """基金历史行情-新浪服务"""
    
    collection_name = "fund_hist_sina"
    provider_class = FundHistSinaProvider
