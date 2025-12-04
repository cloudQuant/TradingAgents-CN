"""中金所上证50指数实时行情数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionCffexSz50SpotSinaService(SimpleService):
    """中金所上证50指数实时行情数据服务"""
    collection_name = "option_cffex_sz50_spot_sina"
