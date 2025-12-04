"""
财报发行服务

百度股市通-财报发行
接口: news_report_time_baidu
"""
from app.services.data_sources.base_service import BaseService
from ..providers.news_report_time_baidu_provider import NewsReportTimeBaiduProvider


class NewsReportTimeBaiduService(BaseService):
    """财报发行服务"""
    
    collection_name = "news_report_time_baidu"
    provider_class = NewsReportTimeBaiduProvider
    
    # 时间字段名
    time_field = "更新时间"
