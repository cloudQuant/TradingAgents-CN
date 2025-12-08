"""COMEX库存数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_comex_inventory_provider import FuturesComexInventoryProvider


class FuturesComexInventoryService(SimpleService):
    """COMEX库存数据服务"""
    collection_name = "futures_comex_inventory"
    provider_class = FuturesComexInventoryProvider
