"""郑州商品交易所-合约信息数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_contract_info_czce_provider import FuturesContractInfoCzceProvider


class FuturesContractInfoCzceService(SimpleService):
    """郑州商品交易所-合约信息数据服务"""
    collection_name = "futures_contract_info_czce"
    provider_class = FuturesContractInfoCzceProvider
