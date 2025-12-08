"""交割统计-大商所数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_delivery_dce_provider import FuturesDeliveryDceProvider


class FuturesDeliveryDceService(SimpleService):
    """交割统计-大商所数据服务"""
    collection_name = "futures_delivery_dce"
    provider_class = FuturesDeliveryDceProvider
