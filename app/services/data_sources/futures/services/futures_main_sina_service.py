"""期货连续合约-新浪服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesMainSinaService(SimpleService):
    """期货连续合约-新浪服务"""
    collection_name = "futures_main_sina"
