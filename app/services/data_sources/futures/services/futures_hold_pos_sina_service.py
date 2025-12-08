"""成交持仓-新浪数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_hold_pos_sina_provider import FuturesHoldPosSinaProvider


class FuturesHoldPosSinaService(SimpleService):
    """成交持仓-新浪数据服务"""
    collection_name = "futures_hold_pos_sina"
    provider_class = FuturesHoldPosSinaProvider
