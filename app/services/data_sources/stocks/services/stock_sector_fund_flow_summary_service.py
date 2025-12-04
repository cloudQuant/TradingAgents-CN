"""
行业个股资金流服务

东方财富网-数据中心-资金流向-行业资金流-xx行业个股资金流
接口: stock_sector_fund_flow_summary
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_sector_fund_flow_summary_provider import StockSectorFundFlowSummaryProvider


class StockSectorFundFlowSummaryService(BaseService):
    """行业个股资金流服务"""
    
    collection_name = "stock_sector_fund_flow_summary"
    provider_class = StockSectorFundFlowSummaryProvider
    
    # 时间字段名
    time_field = "更新时间"
