"""大连商品交易所-合约信息数据服务"""
from app.services.data_sources.base_service import SimpleService


class FuturesContractInfoDceService(SimpleService):
    """大连商品交易所-合约信息数据服务"""
    collection_name = "futures_contract_info_dce"
