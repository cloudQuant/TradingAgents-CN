"""期转现-大商所数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesToSpotDceService(SimpleService):
    """期转现-大商所数据服务"""
    collection_name = "futures_to_spot_dce"
