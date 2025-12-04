"""
关键指标-新浪服务

新浪财经-财务报表-关键指标
接口: stock_financial_abstract
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_financial_abstract_provider import StockFinancialAbstractProvider


class StockFinancialAbstractService(BaseService):
    """关键指标-新浪服务"""
    
    collection_name = "stock_financial_abstract"
    provider_class = StockFinancialAbstractProvider
    
    # 时间字段名
    time_field = "更新时间"
