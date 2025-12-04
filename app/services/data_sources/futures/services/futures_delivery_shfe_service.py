"""交割统计-上期所数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesDeliveryShfeService(SimpleService):
    """交割统计-上期所数据服务"""
    collection_name = "futures_delivery_shfe"
