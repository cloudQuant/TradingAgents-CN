"""期货交易费用参照表数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesFeesInfoService(SimpleService):
    """期货交易费用参照表数据服务"""
    collection_name = "futures_fees_info"
