"""期货合约详情-新浪服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_contract_detail_provider import FuturesContractDetailProvider


class FuturesContractDetailService(SimpleService):
    """期货合约详情-新浪服务"""
    collection_name = "futures_contract_detail"
    provider_class = FuturesContractDetailProvider
