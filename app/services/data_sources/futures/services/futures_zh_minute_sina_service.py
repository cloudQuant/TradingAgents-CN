"""内盘-分时行情数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_zh_minute_sina_provider import FuturesZhMinuteSinaProvider


class FuturesZhMinuteSinaService(SimpleService):
    """内盘-分时行情数据服务"""
    collection_name = "futures_zh_minute_sina"
    provider_class = FuturesZhMinuteSinaProvider
