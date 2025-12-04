"""
证券资料服务

东方财富-港股-证券资料
接口: stock_hk_security_profile_em
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hk_security_profile_em_provider import StockHkSecurityProfileEmProvider


class StockHkSecurityProfileEmService(BaseService):
    """证券资料服务"""
    
    collection_name = "stock_hk_security_profile_em"
    provider_class = StockHkSecurityProfileEmProvider
    
    # 时间字段名
    time_field = "更新时间"
