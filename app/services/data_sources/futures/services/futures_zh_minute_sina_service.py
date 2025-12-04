"""内盘-分时行情数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesZhMinuteSinaService(SimpleService):
    """内盘-分时行情数据服务"""
    collection_name = "futures_zh_minute_sina"
