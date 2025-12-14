"""上期所期权数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_hist_shfe_provider import OptionHistShfeProvider


class OptionHistShfeService(SimpleService):
    """上期所期权数据服务"""
    collection_name = "option_hist_shfe"
    provider_class = OptionHistShfeProvider
