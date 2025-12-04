"""
利润表服务

同花顺-财务指标-利润表
接口: stock_financial_benefit_ths
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_financial_benefit_ths_provider import StockFinancialBenefitThsProvider


class StockFinancialBenefitThsService(BaseService):
    """利润表服务"""
    
    collection_name = "stock_financial_benefit_ths"
    provider_class = StockFinancialBenefitThsProvider
    
    # 时间字段名
    time_field = "更新时间"
