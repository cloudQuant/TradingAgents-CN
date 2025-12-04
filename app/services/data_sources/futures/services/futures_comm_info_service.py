"""期货手续费与保证金数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesCommInfoService(SimpleService):
    """期货手续费与保证金数据服务"""
    collection_name = "futures_comm_info"
