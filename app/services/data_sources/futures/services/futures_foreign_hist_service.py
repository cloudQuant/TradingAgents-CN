"""外盘-历史行情数据-新浪服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesForeignHistService(SimpleService):
    """外盘-历史行情数据-新浪服务"""
    collection_name = "futures_foreign_hist"
