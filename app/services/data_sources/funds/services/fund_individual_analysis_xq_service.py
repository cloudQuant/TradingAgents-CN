"""
基金分析数据-雪球服务（重构版：继承SimpleService）
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.fund_individual_analysis_xq_provider import FundIndividualAnalysisXqProvider


class FundIndividualAnalysisXqService(SimpleService):
    """基金分析数据-雪球服务"""
    
    collection_name = "fund_individual_analysis_xq"
    provider_class = FundIndividualAnalysisXqProvider
