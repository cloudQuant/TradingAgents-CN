"""
利润表-按单季度服务

东方财富-股票-财务分析-利润表-按单季度
接口: stock_profit_sheet_by_quarterly_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_profit_sheet_by_quarterly_em_provider import StockProfitSheetByQuarterlyEmProvider


class StockProfitSheetByQuarterlyEmService(BaseService):
    """利润表-按单季度服务"""
    
    collection_name = "stock_profit_sheet_by_quarterly_em"
    provider_class = StockProfitSheetByQuarterlyEmProvider
    
    # 时间字段名
    time_field = "更新时间"
