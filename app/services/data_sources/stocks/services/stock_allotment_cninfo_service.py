"""
配股实施方案-巨潮资讯服务

巨潮资讯-个股-配股实施方案
接口: stock_allotment_cninfo
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_allotment_cninfo_provider import StockAllotmentCninfoProvider


class StockAllotmentCninfoService(BaseService):
    """配股实施方案-巨潮资讯服务"""
    
    collection_name = "stock_allotment_cninfo"
    provider_class = StockAllotmentCninfoProvider
    
    # 时间字段名
    time_field = "更新时间"
