"""商品期权T型报价表测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionCommodityContractTableSina(OptionsCollectionTestBase):
    """商品期权T型报价表测试类"""
    collection_name = "option_commodity_contract_table_sina"
    display_name = "商品期权T型报价表"
    provider_class_name = "OptionCommodityContractTableSinaProvider"
    service_class_name = "OptionCommodityContractTableSinaService"
    is_simple_provider = False
    required_params = ["symbol"]


if __name__ == "__main__":
    unittest.main()
