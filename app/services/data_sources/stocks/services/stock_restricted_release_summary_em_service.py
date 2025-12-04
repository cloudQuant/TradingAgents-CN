"""
限售股解禁服务

东方财富网-数据中心-特色数据-限售股解禁
接口: stock_restricted_release_summary_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_restricted_release_summary_em_provider import StockRestrictedReleaseSummaryEmProvider


class StockRestrictedReleaseSummaryEmService(BaseService):
    """限售股解禁服务"""
    
    collection_name = "stock_restricted_release_summary_em"
    provider_class = StockRestrictedReleaseSummaryEmProvider
    
    # 时间字段名
    time_field = "更新时间"
