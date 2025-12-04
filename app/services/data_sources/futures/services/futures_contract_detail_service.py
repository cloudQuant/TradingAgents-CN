"""期货合约详情-新浪服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesContractDetailService(SimpleService):
    """期货合约详情-新浪服务"""
    collection_name = "futures_contract_detail"
