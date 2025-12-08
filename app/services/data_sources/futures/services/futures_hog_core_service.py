"""生猪-核心数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_hog_core_provider import FuturesHogCoreProvider


class FuturesHogCoreService(SimpleService):
    """生猪-核心数据服务"""
    collection_name = "futures_hog_core"
    provider_class = FuturesHogCoreProvider
