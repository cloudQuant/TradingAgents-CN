"""郑商所期权数据测试"""
import unittest
from test_base import OptionsCollectionTestBase


class TestOptionHistCzce(OptionsCollectionTestBase):
    """郑商所期权数据测试类"""
    collection_name = "option_hist_czce"
    display_name = "郑商所期权数据"
    provider_class_name = "OptionHistCzceProvider"
    service_class_name = "OptionHistCzceService"
    is_simple_provider = False
    required_params = ["symbol", "date"]


if __name__ == "__main__":
    unittest.main()
