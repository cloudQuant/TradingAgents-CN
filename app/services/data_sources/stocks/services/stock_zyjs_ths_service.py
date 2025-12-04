"""
主营介绍-同花顺服务

同花顺-主营介绍
接口: stock_zyjs_ths
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_zyjs_ths_provider import StockZyjsThsProvider


class StockZyjsThsService(BaseService):
    """主营介绍-同花顺服务"""
    
    collection_name = "stock_zyjs_ths"
    provider_class = StockZyjsThsProvider
    
    # 时间字段名
    time_field = "更新时间"
