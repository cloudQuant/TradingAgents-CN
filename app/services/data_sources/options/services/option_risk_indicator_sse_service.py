"""上交所期权风险指标数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionRiskIndicatorSseService(SimpleService):
    """上交所期权风险指标数据服务"""
    collection_name = "option_risk_indicator_sse"
