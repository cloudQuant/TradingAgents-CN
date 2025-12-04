"""内盘-历史行情数据-东财服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesHistEmService(SimpleService):
    """内盘-历史行情数据-东财服务"""
    collection_name = "futures_hist_em"
