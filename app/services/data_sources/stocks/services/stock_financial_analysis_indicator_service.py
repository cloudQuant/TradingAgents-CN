"""
财务指标服务

新浪财经-财务分析-财务指标
接口: stock_financial_analysis_indicator
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_financial_analysis_indicator_provider import StockFinancialAnalysisIndicatorProvider


class StockFinancialAnalysisIndicatorService(BaseService):
    """财务指标服务"""
    
    collection_name = "stock_financial_analysis_indicator"
    provider_class = StockFinancialAnalysisIndicatorProvider
    
    # 时间字段名
    time_field = "更新时间"
