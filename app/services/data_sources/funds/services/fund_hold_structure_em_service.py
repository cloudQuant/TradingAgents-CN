"""
基金持有结构-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_hold_structure_em_provider import FundHoldStructureEmProvider


class FundHoldStructureEmService(SimpleService):
    """基金持有结构-东财服务"""
    
    collection_name = "fund_hold_structure_em"
    provider_class = FundHoldStructureEmProvider
