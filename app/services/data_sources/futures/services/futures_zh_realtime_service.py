"""内盘-实时行情数据(品种)服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_zh_realtime_provider import FuturesZhRealtimeProvider


class FuturesZhRealtimeService(SimpleService):
    """内盘-实时行情数据(品种)服务"""
    collection_name = "futures_zh_realtime"
    provider_class = FuturesZhRealtimeProvider
