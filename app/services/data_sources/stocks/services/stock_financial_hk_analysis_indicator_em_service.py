"""
港股财务指标服务

东方财富-港股-财务分析-主要指标
接口: stock_financial_hk_analysis_indicator_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_financial_hk_analysis_indicator_em_provider import StockFinancialHkAnalysisIndicatorEmProvider


class StockFinancialHkAnalysisIndicatorEmService(BaseService):
    """港股财务指标服务"""
    
    collection_name = "stock_financial_hk_analysis_indicator_em"
    provider_class = StockFinancialHkAnalysisIndicatorEmProvider
    
    # 时间字段名
    time_field = "更新时间"
