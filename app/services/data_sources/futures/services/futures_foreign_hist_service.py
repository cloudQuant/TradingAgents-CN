"""外盘-历史行情数据-新浪服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_foreign_hist_provider import FuturesForeignHistProvider


class FuturesForeignHistService(SimpleService):
    """外盘-历史行情数据-新浪服务"""
    collection_name = "futures_foreign_hist"
    provider_class = FuturesForeignHistProvider
