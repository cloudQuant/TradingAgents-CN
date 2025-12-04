"""
科创板公告服务

东方财富-科创板报告数据
接口: stock_zh_kcb_report_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zh_kcb_report_em_provider import StockZhKcbReportEmProvider


class StockZhKcbReportEmService(BaseService):
    """科创板公告服务"""
    
    collection_name = "stock_zh_kcb_report_em"
    provider_class = StockZhKcbReportEmProvider
    
    # 时间字段名
    time_field = "更新时间"
