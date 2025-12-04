"""外盘-实时行情数据-东财服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesGlobalSpotEmService(SimpleService):
    """外盘-实时行情数据-东财服务"""
    collection_name = "futures_global_spot_em"
