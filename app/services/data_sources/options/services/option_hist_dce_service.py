"""大商所期权数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_hist_dce_provider import OptionHistDceProvider


class OptionHistDceService(SimpleService):
    """大商所期权数据服务"""
    collection_name = "option_hist_dce"
    provider_class = OptionHistDceProvider
