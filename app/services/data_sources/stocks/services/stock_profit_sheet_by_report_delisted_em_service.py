"""
利润表-按报告期服务

东方财富-股票-财务分析-利润表-已退市股票-按报告期
接口: stock_profit_sheet_by_report_delisted_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_profit_sheet_by_report_delisted_em_provider import StockProfitSheetByReportDelistedEmProvider


class StockProfitSheetByReportDelistedEmService(BaseService):
    """利润表-按报告期服务"""
    
    collection_name = "stock_profit_sheet_by_report_delisted_em"
    provider_class = StockProfitSheetByReportDelistedEmProvider
    
    # 时间字段名
    time_field = "更新时间"
