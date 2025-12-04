"""期货合约详情-东财服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesContractDetailEmService(SimpleService):
    """期货合约详情-东财服务"""
    collection_name = "futures_contract_detail_em"
