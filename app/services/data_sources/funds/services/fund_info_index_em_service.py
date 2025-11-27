"""
指数型基金基本信息-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_info_index_em_provider import FundInfoIndexEmProvider


class FundInfoIndexEmService(SimpleService):
    """指数型基金基本信息-东财服务"""
    
    collection_name = "fund_info_index_em"
    provider_class = FundInfoIndexEmProvider
