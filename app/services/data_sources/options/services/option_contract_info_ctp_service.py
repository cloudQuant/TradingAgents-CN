"""openctp期权合约信息数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionContractInfoCtpService(SimpleService):
    """openctp期权合约信息数据服务"""
    collection_name = "option_contract_info_ctp"
