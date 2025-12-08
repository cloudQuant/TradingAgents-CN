"""现货与股票服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_spot_stock_provider import FuturesSpotStockProvider


class FuturesSpotStockService(SimpleService):
    """现货与股票服务"""
    collection_name = "futures_spot_stock"
    provider_class = FuturesSpotStockProvider
