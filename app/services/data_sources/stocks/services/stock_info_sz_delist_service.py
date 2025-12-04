"""
终止/暂停上市-深证服务

深证证券交易所终止/暂停上市股票
接口: stock_info_sz_delist
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_info_sz_delist_provider import StockInfoSzDelistProvider


class StockInfoSzDelistService(BaseService):
    """终止/暂停上市-深证服务"""
    
    collection_name = "stock_info_sz_delist"
    provider_class = StockInfoSzDelistProvider
    
    # 时间字段名
    time_field = "更新时间"
