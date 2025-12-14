"""商品期权T型报价表数据服务"""
from app.services.data_sources.base_service import SimpleService
from app.services.data_sources.options.providers.option_commodity_contract_table_sina_provider import OptionCommodityContractTableSinaProvider


class OptionCommodityContractTableSinaService(SimpleService):
    """商品期权T型报价表数据服务"""
    collection_name = "option_commodity_contract_table_sina"
    provider_class = OptionCommodityContractTableSinaProvider
