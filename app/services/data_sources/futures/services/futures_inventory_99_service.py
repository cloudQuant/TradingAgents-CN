"""库存数据-99期货网数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_inventory_99_provider import FuturesInventory99Provider


class FuturesInventory99Service(SimpleService):
    """库存数据-99期货网数据服务"""
    collection_name = "futures_inventory_99"
    provider_class = FuturesInventory99Provider
