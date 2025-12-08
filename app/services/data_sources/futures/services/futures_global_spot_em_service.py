"""
外盘-实时行情数据-东财服务

无参数接口，只需要更新功能
"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_global_spot_em_provider import FuturesGlobalSpotEmProvider


class FuturesGlobalSpotEmService(SimpleService):
    """外盘-实时行情数据-东财服务"""
    
    collection_name = "futures_global_spot_em"
    provider_class = FuturesGlobalSpotEmProvider
    
    time_field = "更新时间"
    unique_keys = ["代码"]
