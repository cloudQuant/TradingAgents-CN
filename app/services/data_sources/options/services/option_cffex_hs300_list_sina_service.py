"""中金所沪深300指数合约列表数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_cffex_hs300_list_sina_provider import OptionCffexHs300ListSinaProvider


class OptionCffexHs300ListSinaService(SimpleService):
    """中金所沪深300指数合约列表数据服务"""
    collection_name = "option_cffex_hs300_list_sina"
    provider_class = OptionCffexHs300ListSinaProvider
