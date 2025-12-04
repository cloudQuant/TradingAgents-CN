"""
新股过会服务

巨潮资讯-数据中心-新股数据-新股过会
接口: stock_new_gh_cninfo
"""
from app.services.data_sources.base_service import SimpleService
from ..providers.stock_new_gh_cninfo_provider import StockNewGhCninfoProvider


class StockNewGhCninfoService(SimpleService):
    """新股过会服务"""
    
    collection_name = "stock_new_gh_cninfo"
    provider_class = StockNewGhCninfoProvider
    
    # 时间字段名
    time_field = "更新时间"
