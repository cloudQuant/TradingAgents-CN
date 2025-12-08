"""外盘-实时行情数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_foreign_commodity_realtime_provider import FuturesForeignCommodityRealtimeProvider


class FuturesForeignCommodityRealtimeService(SimpleService):
    """外盘-实时行情数据服务"""
    collection_name = "futures_foreign_commodity_realtime"
    provider_class = FuturesForeignCommodityRealtimeProvider
