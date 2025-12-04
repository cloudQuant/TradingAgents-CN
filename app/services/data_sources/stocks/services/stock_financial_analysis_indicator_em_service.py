"""
主要指标-东方财富服务

东方财富-A股-财务分析-主要指标
接口: stock_financial_analysis_indicator_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_financial_analysis_indicator_em_provider import StockFinancialAnalysisIndicatorEmProvider


class StockFinancialAnalysisIndicatorEmService(BaseService):
    """主要指标-东方财富服务"""
    
    collection_name = "stock_financial_analysis_indicator_em"
    provider_class = StockFinancialAnalysisIndicatorEmProvider
    
    # 时间字段名
    time_field = "更新时间"
