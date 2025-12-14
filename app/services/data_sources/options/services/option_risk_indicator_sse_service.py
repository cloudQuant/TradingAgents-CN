"""上交所期权风险指标数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_risk_indicator_sse_provider import OptionRiskIndicatorSseProvider


class OptionRiskIndicatorSseService(SimpleService):
    """上交所期权风险指标数据服务"""
    collection_name = "option_risk_indicator_sse"
    provider_class = OptionRiskIndicatorSseProvider
