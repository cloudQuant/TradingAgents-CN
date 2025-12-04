"""中金所上证50指数日频行情数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionCffexSz50DailySinaService(SimpleService):
    """中金所上证50指数日频行情数据服务"""
    collection_name = "option_cffex_sz50_daily_sina"
