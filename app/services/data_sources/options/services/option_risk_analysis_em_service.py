"""期权风险分析数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_risk_analysis_em_provider import OptionRiskAnalysisEmProvider


class OptionRiskAnalysisEmService(SimpleService):
    """期权风险分析数据服务"""
    collection_name = "option_risk_analysis_em"
    provider_class = OptionRiskAnalysisEmProvider
