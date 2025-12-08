"""期货合约详情-东财服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_contract_detail_em_provider import FuturesContractDetailEmProvider


class FuturesContractDetailEmService(SimpleService):
    """期货合约详情-东财服务"""
    collection_name = "futures_contract_detail_em"
    provider_class = FuturesContractDetailEmProvider
