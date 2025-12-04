"""
上市相关-巨潮资讯服务

巨潮资讯-个股-上市相关
接口: stock_ipo_summary_cninfo
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_ipo_summary_cninfo_provider import StockIpoSummaryCninfoProvider


class StockIpoSummaryCninfoService(BaseService):
    """上市相关-巨潮资讯服务"""
    
    collection_name = "stock_ipo_summary_cninfo"
    provider_class = StockIpoSummaryCninfoProvider
    
    # 时间字段名
    time_field = "更新时间"
