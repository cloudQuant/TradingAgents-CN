"""内盘-历史行情数据-新浪服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_zh_daily_sina_provider import FuturesZhDailySinaProvider


class FuturesZhDailySinaService(SimpleService):
    """内盘-历史行情数据-新浪服务"""
    collection_name = "futures_zh_daily_sina"
    provider_class = FuturesZhDailySinaProvider
