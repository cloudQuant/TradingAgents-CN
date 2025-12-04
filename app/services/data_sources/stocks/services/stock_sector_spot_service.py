"""
板块行情服务

新浪行业-板块行情
接口: stock_sector_spot
"""
from app.services.data_sources.base_service import BaseService
from ..providers.stock_sector_spot_provider import StockSectorSpotProvider


class StockSectorSpotService(BaseService):
    """板块行情服务"""
    
    collection_name = "stock_sector_spot"
    provider_class = StockSectorSpotProvider
    
    # 时间字段名
    time_field = "更新时间"
