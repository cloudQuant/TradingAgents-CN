"""内盘-实时行情数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_zh_spot_provider import FuturesZhSpotProvider


class FuturesZhSpotService(SimpleService):
    """内盘-实时行情数据服务"""
    collection_name = "futures_zh_spot"
    provider_class = FuturesZhSpotProvider
