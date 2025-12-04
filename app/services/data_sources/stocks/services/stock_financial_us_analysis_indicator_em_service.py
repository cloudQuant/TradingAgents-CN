"""
美股财务指标服务

东方财富-美股-财务分析-主要指标
接口: stock_financial_us_analysis_indicator_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_financial_us_analysis_indicator_em_provider import StockFinancialUsAnalysisIndicatorEmProvider


class StockFinancialUsAnalysisIndicatorEmService(BaseService):
    """美股财务指标服务"""
    
    collection_name = "stock_financial_us_analysis_indicator_em"
    provider_class = StockFinancialUsAnalysisIndicatorEmProvider
    
    # 时间字段名
    time_field = "更新时间"
