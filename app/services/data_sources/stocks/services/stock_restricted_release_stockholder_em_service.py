"""
解禁股东服务

东方财富网-数据中心-个股限售解禁-解禁股东
接口: stock_restricted_release_stockholder_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_restricted_release_stockholder_em_provider import StockRestrictedReleaseStockholderEmProvider


class StockRestrictedReleaseStockholderEmService(BaseService):
    """解禁股东服务"""
    
    collection_name = "stock_restricted_release_stockholder_em"
    provider_class = StockRestrictedReleaseStockholderEmProvider
    
    # 时间字段名
    time_field = "更新时间"
