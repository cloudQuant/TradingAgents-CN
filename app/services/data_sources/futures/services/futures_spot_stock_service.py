"""现货与股票服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesSpotStockService(SimpleService):
    """现货与股票服务"""
    collection_name = "futures_spot_stock"
