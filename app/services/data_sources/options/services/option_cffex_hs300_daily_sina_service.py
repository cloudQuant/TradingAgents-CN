"""中金所沪深300指数日频行情数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionCffexHs300DailySinaService(SimpleService):
    """中金所沪深300指数日频行情数据服务"""
    collection_name = "option_cffex_hs300_daily_sina"
