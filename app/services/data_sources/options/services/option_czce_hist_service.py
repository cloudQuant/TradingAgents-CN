"""郑商所期权历史行情数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_czce_hist_provider import OptionCzceHistProvider


class OptionCzceHistService(SimpleService):
    """郑商所期权历史行情数据服务"""
    collection_name = "option_czce_hist"
    provider_class = OptionCzceHistProvider
