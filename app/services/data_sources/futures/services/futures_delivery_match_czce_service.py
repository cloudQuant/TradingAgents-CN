"""交割配对-郑商所数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesDeliveryMatchCzceService(SimpleService):
    """交割配对-郑商所数据服务"""
    collection_name = "futures_delivery_match_czce"
