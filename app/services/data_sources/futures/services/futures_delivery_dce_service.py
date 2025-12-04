"""交割统计-大商所数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesDeliveryDceService(SimpleService):
    """交割统计-大商所数据服务"""
    collection_name = "futures_delivery_dce"
