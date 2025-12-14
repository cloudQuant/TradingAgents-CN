"""中金所上证50指数合约列表数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_cffex_sz50_list_sina_provider import OptionCffexSz50ListSinaProvider


class OptionCffexSz50ListSinaService(SimpleService):
    """中金所上证50指数合约列表数据服务"""
    collection_name = "option_cffex_sz50_list_sina"
    provider_class = OptionCffexSz50ListSinaProvider
