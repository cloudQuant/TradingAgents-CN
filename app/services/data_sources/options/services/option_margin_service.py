"""期权保证金数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_margin_provider import OptionMarginProvider


class OptionMarginService(SimpleService):
    """期权保证金数据服务"""
    collection_name = "option_margin"
    provider_class = OptionMarginProvider
