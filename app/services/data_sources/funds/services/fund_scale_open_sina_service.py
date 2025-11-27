"""
开放式基金规模-新浪服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_scale_open_sina_provider import FundScaleOpenSinaProvider


class FundScaleOpenSinaService(SimpleService):
    """开放式基金规模-新浪服务"""
    
    collection_name = "fund_scale_open_sina"
    provider_class = FundScaleOpenSinaProvider
