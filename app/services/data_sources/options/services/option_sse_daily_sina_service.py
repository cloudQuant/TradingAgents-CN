"""期权日数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_sse_daily_sina_provider import OptionSseDailySinaProvider


class OptionSseDailySinaService(SimpleService):
    """期权日数据服务"""
    collection_name = "option_sse_daily_sina"
    provider_class = OptionSseDailySinaProvider
