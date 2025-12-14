"""中金所沪深300指数日频行情数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_cffex_hs300_daily_sina_provider import OptionCffexHs300DailySinaProvider


class OptionCffexHs300DailySinaService(SimpleService):
    """中金所沪深300指数日频行情数据服务"""
    collection_name = "option_cffex_hs300_daily_sina"
    provider_class = OptionCffexHs300DailySinaProvider
