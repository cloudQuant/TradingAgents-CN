"""外盘-实时行情数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesForeignCommodityRealtimeService(SimpleService):
    """外盘-实时行情数据服务"""
    collection_name = "futures_foreign_commodity_realtime"
