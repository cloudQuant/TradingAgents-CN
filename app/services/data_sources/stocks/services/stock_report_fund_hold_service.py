"""
基金持股服务

东方财富网-数据中心-主力数据-基金持仓
接口: stock_report_fund_hold
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_report_fund_hold_provider import StockReportFundHoldProvider


class StockReportFundHoldService(BaseService):
    """基金持股服务"""
    
    collection_name = "stock_report_fund_hold"
    provider_class = StockReportFundHoldProvider
    
    # 时间字段名
    time_field = "更新时间"
