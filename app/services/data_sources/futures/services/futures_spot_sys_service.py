"""现期图数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_spot_sys_provider import FuturesSpotSysProvider


class FuturesSpotSysService(SimpleService):
    """现期图数据服务"""
    collection_name = "futures_spot_sys"
    provider_class = FuturesSpotSysProvider
