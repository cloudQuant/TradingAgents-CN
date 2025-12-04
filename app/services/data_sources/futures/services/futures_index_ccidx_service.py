"""中证商品指数服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesIndexCcidxService(SimpleService):
    """中证商品指数服务"""
    collection_name = "futures_index_ccidx"
