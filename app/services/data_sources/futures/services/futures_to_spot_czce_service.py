"""期转现-郑商所数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesToSpotCzceService(SimpleService):
    """期转现-郑商所数据服务"""
    collection_name = "futures_to_spot_czce"
