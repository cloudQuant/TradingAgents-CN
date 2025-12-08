"""期货连续合约-新浪服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_main_sina_provider import FuturesMainSinaProvider


class FuturesMainSinaService(SimpleService):
    """期货连续合约-新浪服务"""
    collection_name = "futures_main_sina"
    provider_class = FuturesMainSinaProvider
