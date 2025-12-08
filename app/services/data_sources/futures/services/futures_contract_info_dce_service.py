"""
大连商品交易所-合约信息数据服务

无参数接口，只需要更新功能
"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_contract_info_dce_provider import FuturesContractInfoDceProvider


class FuturesContractInfoDceService(SimpleService):
    """大连商品交易所-合约信息数据服务"""
    
    collection_name = "futures_contract_info_dce"
    provider_class = FuturesContractInfoDceProvider
    
    time_field = "更新时间"
    unique_keys = ["合约代码"]
