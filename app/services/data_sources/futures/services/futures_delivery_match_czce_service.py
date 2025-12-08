"""交割配对-郑商所数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_delivery_match_czce_provider import FuturesDeliveryMatchCzceProvider


class FuturesDeliveryMatchCzceService(SimpleService):
    """交割配对-郑商所数据服务"""
    collection_name = "futures_delivery_match_czce"
    provider_class = FuturesDeliveryMatchCzceProvider
