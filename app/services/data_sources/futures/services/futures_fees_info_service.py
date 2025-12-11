"""
期货交易费用参照表数据服务

无参数接口，只需要更新功能，不需要批量更新
"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_fees_info_provider import FuturesFeesInfoProvider


class FuturesFeesInfoService(SimpleService):
    """期货交易费用参照表数据服务"""
    
    collection_name = "futures_fees_info"
    provider_class = FuturesFeesInfoProvider
    
    time_field = "更新时间"
    unique_keys = ["日期", "合约代码"]
