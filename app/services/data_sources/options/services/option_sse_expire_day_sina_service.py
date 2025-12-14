"""剩余到期时间数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_sse_expire_day_sina_provider import OptionSseExpireDaySinaProvider


class OptionSseExpireDaySinaService(SimpleService):
    """剩余到期时间数据服务"""
    collection_name = "option_sse_expire_day_sina"
    provider_class = OptionSseExpireDaySinaProvider
