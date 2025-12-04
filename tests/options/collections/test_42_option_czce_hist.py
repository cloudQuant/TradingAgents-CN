"""郑商所期权历史行情测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionCzceHist(OptionsCollectionTestBase):
    """郑商所期权历史行情测试类"""
    collection_name = "option_czce_hist"
    display_name = "郑商所期权历史行情"
    provider_class_name = "OptionCzceHistProvider"
    service_class_name = "OptionCzceHistService"
    is_simple_provider = False
    required_params = ["symbol"]


if __name__ == "__main__":
    unittest.main()
