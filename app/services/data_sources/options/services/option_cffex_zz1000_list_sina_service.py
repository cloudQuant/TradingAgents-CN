"""中金所中证1000指数合约列表数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_cffex_zz1000_list_sina_provider import OptionCffexZz1000ListSinaProvider


class OptionCffexZz1000ListSinaService(SimpleService):
    """中金所中证1000指数合约列表数据服务"""
    collection_name = "option_cffex_zz1000_list_sina"
    provider_class = OptionCffexZz1000ListSinaProvider
