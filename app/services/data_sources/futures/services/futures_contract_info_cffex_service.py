"""中国金融期货交易所-合约信息数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.futures.providers.futures_contract_info_cffex_provider import FuturesContractInfoCffexProvider


class FuturesContractInfoCffexService(SimpleService):
    """中国金融期货交易所-合约信息数据服务"""
    collection_name = "futures_contract_info_cffex"
    provider_class = FuturesContractInfoCffexProvider
