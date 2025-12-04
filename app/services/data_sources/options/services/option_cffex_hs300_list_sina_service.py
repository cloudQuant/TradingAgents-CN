"""中金所沪深300指数合约列表数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionCffexHs300ListSinaService(SimpleService):
    """中金所沪深300指数合约列表数据服务"""
    collection_name = "option_cffex_hs300_list_sina"
