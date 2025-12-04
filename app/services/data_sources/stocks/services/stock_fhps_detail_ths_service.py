"""
分红情况-同花顺服务

同花顺-分红情况
接口: stock_fhps_detail_ths
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_fhps_detail_ths_provider import StockFhpsDetailThsProvider


class StockFhpsDetailThsService(BaseService):
    """分红情况-同花顺服务"""
    
    collection_name = "stock_fhps_detail_ths"
    provider_class = StockFhpsDetailThsProvider
    
    # 时间字段名
    time_field = "更新时间"
