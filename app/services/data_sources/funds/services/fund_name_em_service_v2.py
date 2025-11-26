"""
基金基本信息-东财服务 (使用基类重构版本)

对比原版本 fund_name_em_service.py（109行），新版本只需要约10行代码。
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_name_em_provider_v2 import FundNameEmProviderV2


class FundNameEmServiceV2(SimpleService):
    """基金基本信息-东财服务"""
    
    collection_name = "fund_name_em"
    provider_class = FundNameEmProviderV2
