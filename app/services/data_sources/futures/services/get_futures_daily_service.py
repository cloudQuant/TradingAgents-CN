"""内盘-历史行情数据-交易所服务"""
from app.services.data_sources.base_service import SimpleService


class GetFuturesDailyService(SimpleService):
    """内盘-历史行情数据-交易所服务"""
    collection_name = "get_futures_daily"
