"""中金所中证1000指数日频行情数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_cffex_zz1000_daily_sina_provider import OptionCffexZz1000DailySinaProvider


class OptionCffexZz1000DailySinaService(SimpleService):
    """中金所中证1000指数日频行情数据服务"""
    collection_name = "option_cffex_zz1000_daily_sina"
    provider_class = OptionCffexZz1000DailySinaProvider
