"""交割统计-郑商所数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesDeliveryCzceService(SimpleService):
    """交割统计-郑商所数据服务"""
    collection_name = "futures_delivery_czce"
