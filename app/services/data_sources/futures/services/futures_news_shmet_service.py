"""期货资讯服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_news_shmet_provider import FuturesNewsShmetProvider


class FuturesNewsShmetService(SimpleService):
    """期货资讯服务"""
    collection_name = "futures_news_shmet"
    provider_class = FuturesNewsShmetProvider
