"""交割配对-大商所数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_delivery_match_dce_provider import FuturesDeliveryMatchDceProvider


class FuturesDeliveryMatchDceService(SimpleService):
    """交割配对-大商所数据服务"""
    collection_name = "futures_delivery_match_dce"
    provider_class = FuturesDeliveryMatchDceProvider
