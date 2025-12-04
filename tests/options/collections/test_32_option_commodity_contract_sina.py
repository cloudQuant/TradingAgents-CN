"""商品期权当前合约测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionCommodityContractSina(OptionsCollectionTestBase):
    """商品期权当前合约测试类"""
    collection_name = "option_commodity_contract_sina"
    display_name = "商品期权当前合约"
    provider_class_name = "OptionCommodityContractSinaProvider"
    service_class_name = "OptionCommodityContractSinaService"
    is_simple_provider = False
    required_params = ["symbol"]


if __name__ == "__main__":
    unittest.main()
