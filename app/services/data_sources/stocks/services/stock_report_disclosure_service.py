"""
预约披露时间-巨潮资讯服务

巨潮资讯-数据-预约披露的数据
接口: stock_report_disclosure
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_report_disclosure_provider import StockReportDisclosureProvider


class StockReportDisclosureService(BaseService):
    """预约披露时间-巨潮资讯服务"""
    
    collection_name = "stock_report_disclosure"
    provider_class = StockReportDisclosureProvider
    
    # 时间字段名
    time_field = "更新时间"
