"""期权价值分析数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_value_analysis_em_provider import OptionValueAnalysisEmProvider


class OptionValueAnalysisEmService(SimpleService):
    """期权价值分析数据服务"""
    collection_name = "option_value_analysis_em"
    provider_class = OptionValueAnalysisEmProvider
