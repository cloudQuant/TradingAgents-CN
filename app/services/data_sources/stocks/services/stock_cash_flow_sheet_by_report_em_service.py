"""
现金流量表-按报告期服务

东方财富-股票-财务分析-现金流量表-按报告期
接口: stock_cash_flow_sheet_by_report_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_cash_flow_sheet_by_report_em_provider import StockCashFlowSheetByReportEmProvider


class StockCashFlowSheetByReportEmService(BaseService):
    """现金流量表-按报告期服务"""
    
    collection_name = "stock_cash_flow_sheet_by_report_em"
    provider_class = StockCashFlowSheetByReportEmProvider
    
    # 时间字段名
    time_field = "更新时间"
