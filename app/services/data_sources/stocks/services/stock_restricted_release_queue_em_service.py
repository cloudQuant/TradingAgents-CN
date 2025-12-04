"""
解禁批次服务

东方财富网-数据中心-个股限售解禁-解禁批次
接口: stock_restricted_release_queue_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_restricted_release_queue_em_provider import StockRestrictedReleaseQueueEmProvider


class StockRestrictedReleaseQueueEmService(BaseService):
    """解禁批次服务"""
    
    collection_name = "stock_restricted_release_queue_em"
    provider_class = StockRestrictedReleaseQueueEmProvider
    
    # 时间字段名
    time_field = "更新时间"
