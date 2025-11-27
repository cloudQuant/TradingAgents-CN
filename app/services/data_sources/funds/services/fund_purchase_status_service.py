"""
基金申购状态-东财服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_purchase_status_provider import FundPurchaseStatusProvider


class FundPurchaseStatusService(SimpleService):
    """基金申购状态-东财服务"""
    
    collection_name = "fund_purchase_status"
    provider_class = FundPurchaseStatusProvider
