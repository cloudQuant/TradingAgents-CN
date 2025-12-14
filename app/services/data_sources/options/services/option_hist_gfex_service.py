"""广期所期权数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_hist_gfex_provider import OptionHistGfexProvider


class OptionHistGfexService(SimpleService):
    """广期所期权数据服务"""
    collection_name = "option_hist_gfex"
    provider_class = OptionHistGfexProvider
