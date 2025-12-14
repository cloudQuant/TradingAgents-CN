"""商品期权当前合约数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_commodity_contract_sina_provider import OptionCommodityContractSinaProvider


class OptionCommodityContractSinaService(SimpleService):
    """商品期权当前合约数据服务"""
    collection_name = "option_commodity_contract_sina"
    provider_class = OptionCommodityContractSinaProvider
