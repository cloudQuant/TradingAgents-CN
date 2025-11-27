"""
封闭式基金规模-新浪服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_scale_close_sina_provider import FundScaleCloseSinaProvider


class FundScaleCloseSinaService(SimpleService):
    """封闭式基金规模-新浪服务"""
    
    collection_name = "fund_scale_close_sina"
    provider_class = FundScaleCloseSinaProvider
