"""
个股限售解禁-新浪服务

新浪财经-发行分配-限售解禁
接口: stock_restricted_release_queue_sina
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_restricted_release_queue_sina_provider import StockRestrictedReleaseQueueSinaProvider


class StockRestrictedReleaseQueueSinaService(BaseService):
    """个股限售解禁-新浪服务"""
    
    collection_name = "stock_restricted_release_queue_sina"
    provider_class = StockRestrictedReleaseQueueSinaProvider
    
    # 时间字段名
    time_field = "更新时间"
