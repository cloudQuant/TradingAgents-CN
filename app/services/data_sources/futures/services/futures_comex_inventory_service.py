"""COMEX库存数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesComexInventoryService(SimpleService):
    """COMEX库存数据服务"""
    collection_name = "futures_comex_inventory"
