"""openctp期权合约信息数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_contract_info_ctp_provider import OptionContractInfoCtpProvider


class OptionContractInfoCtpService(SimpleService):
    """openctp期权合约信息数据服务"""
    collection_name = "option_contract_info_ctp"
    provider_class = OptionContractInfoCtpProvider
