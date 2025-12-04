"""
关键指标-同花顺服务

同花顺-财务指标-主要指标
接口: stock_financial_abstract_ths
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_financial_abstract_ths_provider import StockFinancialAbstractThsProvider


class StockFinancialAbstractThsService(BaseService):
    """关键指标-同花顺服务"""
    
    collection_name = "stock_financial_abstract_ths"
    provider_class = StockFinancialAbstractThsProvider
    
    # 时间字段名
    time_field = "更新时间"
