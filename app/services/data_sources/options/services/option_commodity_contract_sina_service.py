"""商品期权当前合约数据服务"""
from app.services.data_sources.base_service import SimpleService


class OptionCommodityContractSinaService(SimpleService):
    """商品期权当前合约数据服务"""
    collection_name = "option_commodity_contract_sina"
