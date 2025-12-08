"""上海期货交易所-合约信息数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_contract_info_shfe_provider import FuturesContractInfoShfeProvider


class FuturesContractInfoShfeService(SimpleService):
    """上海期货交易所-合约信息数据服务"""
    collection_name = "futures_contract_info_shfe"
    provider_class = FuturesContractInfoShfeProvider
