"""交割统计-郑商所数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_delivery_czce_provider import FuturesDeliveryCzceProvider


class FuturesDeliveryCzceService(SimpleService):
    """交割统计-郑商所数据服务"""
    collection_name = "futures_delivery_czce"
    provider_class = FuturesDeliveryCzceProvider
