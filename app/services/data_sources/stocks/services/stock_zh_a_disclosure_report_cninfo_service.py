"""
信息披露公告-巨潮资讯服务

巨潮资讯-首页-公告查询-信息披露公告-沪深京
接口: stock_zh_a_disclosure_report_cninfo
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zh_a_disclosure_report_cninfo_provider import StockZhADisclosureReportCninfoProvider


class StockZhADisclosureReportCninfoService(BaseService):
    """信息披露公告-巨潮资讯服务"""
    
    collection_name = "stock_zh_a_disclosure_report_cninfo"
    provider_class = StockZhADisclosureReportCninfoProvider
    
    # 时间字段名
    time_field = "更新时间"
