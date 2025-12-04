"""期权折溢价数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionPremiumAnalysisEmService(SimpleService):
    """期权折溢价数据服务"""
    collection_name = "option_premium_analysis_em"
