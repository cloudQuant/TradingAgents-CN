"""中金所中证1000指数实时行情数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_cffex_zz1000_spot_sina_provider import OptionCffexZz1000SpotSinaProvider


class OptionCffexZz1000SpotSinaService(SimpleService):
    """中金所中证1000指数实时行情数据服务"""
    collection_name = "option_cffex_zz1000_spot_sina"
    provider_class = OptionCffexZz1000SpotSinaProvider
