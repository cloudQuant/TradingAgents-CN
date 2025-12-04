"""
名称变更-深证服务

深证证券交易所-市场数据-股票数据-名称变更
接口: stock_info_sz_change_name
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_info_sz_change_name_provider import StockInfoSzChangeNameProvider


class StockInfoSzChangeNameService(BaseService):
    """名称变更-深证服务"""
    
    collection_name = "stock_info_sz_change_name"
    provider_class = StockInfoSzChangeNameProvider
    
    # 时间字段名
    time_field = "更新时间"
