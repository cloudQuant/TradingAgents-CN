"""
利润表-按年度服务

东方财富-股票-财务分析-利润表-按年度
接口: stock_profit_sheet_by_yearly_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_profit_sheet_by_yearly_em_provider import StockProfitSheetByYearlyEmProvider


class StockProfitSheetByYearlyEmService(BaseService):
    """利润表-按年度服务"""
    
    collection_name = "stock_profit_sheet_by_yearly_em"
    provider_class = StockProfitSheetByYearlyEmProvider
    
    # 时间字段名
    time_field = "更新时间"
