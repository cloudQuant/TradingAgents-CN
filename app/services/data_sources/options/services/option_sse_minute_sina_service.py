"""期权分钟数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_sse_minute_sina_provider import OptionSseMinuteSinaProvider


class OptionSseMinuteSinaService(SimpleService):
    """期权分钟数据服务"""
    collection_name = "option_sse_minute_sina"
    provider_class = OptionSseMinuteSinaProvider
