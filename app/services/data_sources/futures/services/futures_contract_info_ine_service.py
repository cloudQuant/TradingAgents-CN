"""上海国际能源交易中心-合约信息数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_contract_info_ine_provider import FuturesContractInfoIneProvider


class FuturesContractInfoIneService(SimpleService):
    """上海国际能源交易中心-合约信息数据服务"""
    collection_name = "futures_contract_info_ine"
    provider_class = FuturesContractInfoIneProvider
