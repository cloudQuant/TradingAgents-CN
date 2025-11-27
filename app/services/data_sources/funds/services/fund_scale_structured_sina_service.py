"""
分级基金规模-新浪服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_scale_structured_sina_provider import FundScaleStructuredSinaProvider


class FundScaleStructuredSinaService(SimpleService):
    """分级基金规模-新浪服务"""
    
    collection_name = "fund_scale_structured_sina"
    provider_class = FundScaleStructuredSinaProvider
