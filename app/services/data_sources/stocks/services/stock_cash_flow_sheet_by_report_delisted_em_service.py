"""
现金流量表-按报告期服务

东方财富-股票-财务分析-现金流量表-已退市股票-按报告期
接口: stock_cash_flow_sheet_by_report_delisted_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_cash_flow_sheet_by_report_delisted_em_provider import StockCashFlowSheetByReportDelistedEmProvider


class StockCashFlowSheetByReportDelistedEmService(BaseService):
    """现金流量表-按报告期服务"""
    
    collection_name = "stock_cash_flow_sheet_by_report_delisted_em"
    provider_class = StockCashFlowSheetByReportDelistedEmProvider
    
    # 时间字段名
    time_field = "更新时间"
