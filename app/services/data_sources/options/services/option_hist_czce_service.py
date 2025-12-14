"""郑商所期权数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_hist_czce_provider import OptionHistCzceProvider


class OptionHistCzceService(SimpleService):
    """郑商所期权数据服务"""
    collection_name = "option_hist_czce"
    provider_class = OptionHistCzceProvider
