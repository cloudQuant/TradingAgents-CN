"""
基金经理-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_manager_em_provider import FundManagerEmProvider


class FundManagerEmService(SimpleService):
    """基金经理-东财服务"""
    
    collection_name = "fund_manager_em"
    provider_class = FundManagerEmProvider
