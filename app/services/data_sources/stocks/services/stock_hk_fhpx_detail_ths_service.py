"""
分红配送详情-港股-同花顺服务

同花顺-港股-分红派息
接口: stock_hk_fhpx_detail_ths
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_hk_fhpx_detail_ths_provider import StockHkFhpxDetailThsProvider


class StockHkFhpxDetailThsService(BaseService):
    """分红配送详情-港股-同花顺服务"""
    
    collection_name = "stock_hk_fhpx_detail_ths"
    provider_class = StockHkFhpxDetailThsProvider
    
    # 时间字段名
    time_field = "更新时间"
