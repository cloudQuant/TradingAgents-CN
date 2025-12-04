"""
公司概况-巨潮资讯服务

巨潮资讯-个股-公司概况
接口: stock_profile_cninfo
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_profile_cninfo_provider import StockProfileCninfoProvider


class StockProfileCninfoService(BaseService):
    """公司概况-巨潮资讯服务"""
    
    collection_name = "stock_profile_cninfo"
    provider_class = StockProfileCninfoProvider
    
    # 时间字段名
    time_field = "更新时间"
