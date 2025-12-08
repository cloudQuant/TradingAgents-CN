"""期货手续费与保证金数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_comm_info_provider import FuturesCommInfoProvider


class FuturesCommInfoService(SimpleService):
    """期货手续费与保证金数据服务"""
    collection_name = "futures_comm_info"
    provider_class = FuturesCommInfoProvider
