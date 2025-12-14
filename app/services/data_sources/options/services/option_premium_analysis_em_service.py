"""期权折溢价数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_premium_analysis_em_provider import OptionPremiumAnalysisEmProvider


class OptionPremiumAnalysisEmService(SimpleService):
    """期权折溢价数据服务"""
    collection_name = "option_premium_analysis_em"
    provider_class = OptionPremiumAnalysisEmProvider
