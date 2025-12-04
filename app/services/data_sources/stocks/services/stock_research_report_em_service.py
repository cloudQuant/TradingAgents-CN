"""
个股研报服务

东方财富网-数据中心-研究报告-个股研报
接口: stock_research_report_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_research_report_em_provider import StockResearchReportEmProvider


class StockResearchReportEmService(BaseService):
    """个股研报服务"""
    
    collection_name = "stock_research_report_em"
    provider_class = StockResearchReportEmProvider
    
    # 时间字段名
    time_field = "更新时间"
