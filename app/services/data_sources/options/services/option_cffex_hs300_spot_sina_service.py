"""中金所沪深300指数实时行情数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_cffex_hs300_spot_sina_provider import OptionCffexHs300SpotSinaProvider


class OptionCffexHs300SpotSinaService(SimpleService):
    """中金所沪深300指数实时行情数据服务"""
    collection_name = "option_cffex_hs300_spot_sina"
    provider_class = OptionCffexHs300SpotSinaProvider
