"""库存数据-99期货网数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesInventory99Service(SimpleService):
    """库存数据-99期货网数据服务"""
    collection_name = "futures_inventory_99"
