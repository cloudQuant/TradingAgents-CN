"""现期图数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesSpotSysService(SimpleService):
    """现期图数据服务"""
    collection_name = "futures_spot_sys"
