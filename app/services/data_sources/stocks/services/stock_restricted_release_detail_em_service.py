"""
限售股解禁详情服务

东方财富网-数据中心-限售股解禁-解禁详情一览
接口: stock_restricted_release_detail_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_restricted_release_detail_em_provider import StockRestrictedReleaseDetailEmProvider


class StockRestrictedReleaseDetailEmService(BaseService):
    """限售股解禁详情服务"""
    
    collection_name = "stock_restricted_release_detail_em"
    provider_class = StockRestrictedReleaseDetailEmProvider
    
    # 时间字段名
    time_field = "更新时间"
