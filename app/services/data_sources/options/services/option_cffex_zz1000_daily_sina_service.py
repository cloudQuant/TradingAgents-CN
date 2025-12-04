"""中金所中证1000指数日频行情数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionCffexZz1000DailySinaService(SimpleService):
    """中金所中证1000指数日频行情数据服务"""
    collection_name = "option_cffex_zz1000_daily_sina"
