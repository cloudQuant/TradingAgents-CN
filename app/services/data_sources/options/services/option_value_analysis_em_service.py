"""期权价值分析数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionValueAnalysisEmService(SimpleService):
    """期权价值分析数据服务"""
    collection_name = "option_value_analysis_em"
