"""上海期货交易所-合约信息数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesContractInfoShfeService(SimpleService):
    """上海期货交易所-合约信息数据服务"""
    collection_name = "futures_contract_info_shfe"
