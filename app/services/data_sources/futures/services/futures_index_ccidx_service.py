"""中证商品指数服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_index_ccidx_provider import FuturesIndexCcidxProvider


class FuturesIndexCcidxService(SimpleService):
    """中证商品指数服务"""
    collection_name = "futures_index_ccidx"
    provider_class = FuturesIndexCcidxProvider
