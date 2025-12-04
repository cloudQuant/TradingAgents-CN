"""库存数据-东方财富数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesInventoryEmService(SimpleService):
    """库存数据-东方财富数据服务"""
    collection_name = "futures_inventory_em"
