"""
基金持股明细服务

东方财富网-数据中心-主力数据-基金持仓-基金持仓明细表
接口: stock_report_fund_hold_detail
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_report_fund_hold_detail_provider import StockReportFundHoldDetailProvider


class StockReportFundHoldDetailService(BaseService):
    """基金持股明细服务"""
    
    collection_name = "stock_report_fund_hold_detail"
    provider_class = StockReportFundHoldDetailProvider
    
    # 时间字段名
    time_field = "更新时间"
