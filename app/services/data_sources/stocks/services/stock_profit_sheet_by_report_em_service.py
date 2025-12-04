"""
利润表-按报告期服务

东方财富-股票-财务分析-利润表-报告期
接口: stock_profit_sheet_by_report_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_profit_sheet_by_report_em_provider import StockProfitSheetByReportEmProvider


class StockProfitSheetByReportEmService(BaseService):
    """利润表-按报告期服务"""
    
    collection_name = "stock_profit_sheet_by_report_em"
    provider_class = StockProfitSheetByReportEmProvider
    
    # 时间字段名
    time_field = "更新时间"
