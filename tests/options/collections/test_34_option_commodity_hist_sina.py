"""商品期权历史行情测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionCommodityHistSina(OptionsCollectionTestBase):
    """商品期权历史行情测试类"""
    collection_name = "option_commodity_hist_sina"
    display_name = "商品期权历史行情"
    provider_class_name = "OptionCommodityHistSinaProvider"
    service_class_name = "OptionCommodityHistSinaService"
    is_simple_provider = False
    required_params = ["symbol"]


if __name__ == "__main__":
    unittest.main()
